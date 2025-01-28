{% extends 'base.tpl' %}
{% block title %}週7日本語{% endblock %}
{% block content %}
  <div class="fs-5 pt-1 pb-3 max-vw-20">
    <img src="{{ str_RelativePath('/static/img/main_visual.svg', str_Cwd) }}" class="img-fluid w-100 py-5" transition-style="in:wipe:curtain" alt="週7日本語 メインビジュアル">
    <div transition-style="in:fade">
      <p class="text-center fs-2 py-2">週7日本語は日本語のボキャブラリーを日々培うことを目的としたブラウザ型暗記カードです。</p>
      <p class="text-center fs-5 py-2">曜日ごとに違ったカードの束（Bunch）を用意しています。各曜日の午前6時になると、自動で内容が更新されます。</p>
      <p class="text-center fs-5 py-2">よく知っているような言葉でも、簡単な文章で説明するのは難しいということがあります。週7日本語を使って、身近な言葉から難解な言葉まで幅広い語彙力を手に入れましょう！</p>
      <div class="d-grid col-9 col-sm-7 col-lg-6 col-xl-5 mx-auto py-2">
        {% set str_todayBunchAbsPath = '/bunch/' ~ lst_Days[int_TodayId]['symbol'] %} {# 引数absoluteとして渡す変数str_todayBunchAbsPathを設定 #}
        <a class="btn btn-secondary align-baseline fs-2 px-2 rounded-4" href="{{ str_RelativePath(str_todayBunchAbsPath, str_Cwd) }}" style="font-family: 'YakuHanMPs', 'Noto Serif JP', serif; font-weight: 900;">
          本日の束へ
          <i class="bi bi-rocket-takeoff-fill"></i>
        </a>
      </div>
      <br>
      <p class="text-center fs-6">※ 更新はジャンルごとに決まった数だけデータベースから無作為に抽出しておこなっています。そのため、同じカードが連日収録されることがあるのをご了承ください。</p>
      <p class="text-center fs-6">※ カードに記載されている説明および例文は、辞書等を参照しながらも ky5bass が個人的な趣味の範疇で作成したものであり、誤り等が含まれていることがあります。あらかじめご理解願います。</p>
    </div>
  </div>
{% endblock %}