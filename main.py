from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from supabase import create_client
import shutil
from os.path import relpath
from os import environ
from datetime import timedelta
from datetime import datetime as _datetime

str_SupabaseUrl = environ['SUPABASE_URL']
str_SupabaseKey = environ['SUPABASE_KEY']

objPath_DistDir = Path(__file__).parent / 'public'  # 注 このディレクトリの中身は空であるものとして以下進める
objPath_SrcDir  = Path(__file__).parent / 'static'
objPath_TplDir  = Path(__file__).parent / 'templates'

# 曜日リスト
lst_Days = [ { "symbol": "sun", "name_ja": "日曜日", },
             { "symbol": "mon", "name_ja": "月曜日", },
             { "symbol": "tue", "name_ja": "火曜日", },
             { "symbol": "wed", "name_ja": "水曜日", },
             { "symbol": "thu", "name_ja": "木曜日", },
             { "symbol": "fri", "name_ja": "金曜日", },
             { "symbol": "sat", "name_ja": "土曜日", }, ]

# supabaseクライアント
objClient_Supabase = create_client(str_SupabaseUrl, str_SupabaseKey)

def str_RelativePath(
    str_Absolute: str,
    str_Cwd: str,
) -> str:
    """cwdに対するabsoluteの相対パスを取得"""

    # 引数のバリデーションチェック
    if '/' != str_Absolute[0]: raise ValueError(f"argument 'absolute' must start with '/': {str_Absolute}")
    if '/' != str_Cwd[0]:      raise ValueError(f"argument 'cwd' must start with '/': {str_Cwd}")
    
    # 相対パスを取得
    str_Ret = relpath(str_Absolute, str_Cwd)

    return str_Ret

def main():
    # ソースディレクトリを丸ごとコピー
    shutil.copytree(objPath_SrcDir, objPath_DistDir / objPath_SrcDir.name)

    # 出力先ディレクトリ内にbunchディレクトリを作成
    objPath_TargetDir = objPath_DistDir / 'bunch'
    objPath_TargetDir.mkdir()
    for dct_Day in lst_Days:
        str_TargetDaySymbol = dct_Day["symbol"]
        objPath_TargetDir = objPath_DistDir / f'bunch/{str_TargetDaySymbol}'
        objPath_TargetDir.mkdir()

    # すべての束の情報を取得
    objResp_Db_0 = ( objClient_Supabase.table('bunches')
                                       .select('*')
                                       .order('day_id')
                                       .execute() )
    # 参考 https://supabase.com/docs/reference/python/select
    lst_Bunches = [{}, {}, {}, {}, {}, {}, {}]  # 注 7つの空辞書はday_id=0〜6に対応
    for objEntry in objResp_Db_0.data:
        int_DayId: int = objEntry['day_id']
        str_UpdatedAt_Raw: str = objEntry['updated_at']
        objDtm_UpdatedAt = _datetime.strptime(str_UpdatedAt_Raw, r'%Y-%m-%d')
        lst_Bunches[int_DayId]['updated_at'] = objDtm_UpdatedAt
        # 注 ↑の処理はbunchesにday_id=0〜6のレコードが格納されている前提で実装している

    # レンダリングの準備
    objEnv = Environment(loader=FileSystemLoader(objPath_TplDir), trim_blocks=False)
    objEnv.globals['str_RelativePath'] = str_RelativePath   # テンプレにrelative_path関数を埋め込み
    # 参考 関数埋め込みの方法→ https://gist.github.com/snaka/2575718
    objEnv.globals['lst_Days'] = lst_Days                   # テンプレにコンテクストとしてlst_Daysを渡す

    # 本日のdayIdを取得
    objDtm_now = _datetime.now() + timedelta(hours=+9)
    # 注 9時間後にすることで日本時間に変換
    int_TodayId = (objDtm_now.weekday() + 1) % 7
    # 注 <datetime object>.weekday() -> 0(月曜), ..., 6(日曜)

    # トップページをレンダリング
    objTemplate = objEnv.get_template('index.tpl')
    str_Output = objTemplate.render(int_TodayId=int_TodayId,
                                     str_Cwd='/',)
    objPath_Output = objPath_DistDir / 'index.html'
    with objPath_Output.open('wt') as objFile_Output:
        objFile_Output.write(str_Output)
    # 参考 extendsの方法→ https://www.python.ambitious-engineer.com/archives/809

    for int_DayId, dct_Day in enumerate(lst_Days):
        # 曜日に対応する束のカードを取得
        objResp_Db_1 = ( objClient_Supabase.rpc('bunch', params={'_day_id': int_DayId})
                                           .order('number')
                                           .execute() )
        # 参考 https://supabase.com/docs/reference/python/rpc
        lst_Cards: list = objResp_Db_1.data

        # 更新日付を取得
        dct_Bunch = lst_Bunches[int_DayId]
        objDtm_UpdatedAt = dct_Bunch['updated_at']
        str_Date = objDtm_UpdatedAt.strftime(r'%Y年%-m月%-d日')
        # 注 %-m %-d で月日を1桁で表現できる。ただしUnix環境に依存しており、Windowsなら %#m %#d らしい。
        #    参考 https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0#answer-2073189

        # bunchページをレンダリング
        objTemplate = objEnv.get_template('bunch.tpl')
        str_Output = objTemplate.render(lst_Cards=lst_Cards,
                                         str_UpdatedDate=str_Date,
                                         int_TargetDayId=int_DayId,
                                         str_Cwd='/bunch', )
        str_TargetDaySymbol = dct_Day['symbol']
        objPath_Output = objPath_DistDir / f'bunch/{str_TargetDaySymbol}/index.html'
        with objPath_Output.open('wt') as objFile_Output:
            objFile_Output.write(str_Output)

if __name__ == '__main__':
    main()