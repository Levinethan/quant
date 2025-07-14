import os
import pandas as pd
import glob

def merge_test_val(src_dir='src', val_dir='validation_sets', out_dir='output'):
    os.makedirs(out_dir, exist_ok=True)
    # 获取src目录下所有csv文件（不含_val）
    src_files = [f for f in glob.glob(os.path.join(src_dir, '*.csv')) if not f.endswith('_val.csv')]
    merged_count = 0
    total = 0

    for src_file in src_files:
        base = os.path.basename(src_file)
        # 构造验证集文件名
        val_file = os.path.join(val_dir, base.replace('.csv', '_val.csv'))
        total += 1
        if not os.path.exists(val_file):
            print(f"⚠️ 未找到验证集: {val_file}")
            continue

        # 读取数据
        df_test = pd.read_csv(src_file)
        df_val = pd.read_csv(val_file)
        # 合并并去重
        df_merged = pd.concat([df_test, df_val], ignore_index=True)
        if 'start_time' in df_merged.columns:
            df_merged['start_time'] = pd.to_datetime(df_merged['start_time'])
            df_merged = df_merged.sort_values('start_time').drop_duplicates('start_time')
        # 输出
        out_file = os.path.join(out_dir, base)
        df_merged.to_csv(out_file, index=False)
        print(f"✅ 合并完成: {out_file}")
        merged_count += 1

    print(f"\n🎉 共合并 {merged_count}/{total} 对测试集+验证集文件，输出目录: {out_dir}")

if __name__ == '__main__':
    merge_test_val() 
