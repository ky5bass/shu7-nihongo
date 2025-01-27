{% extends 'base.tpl' %}
{% block title %}{{ lst_Days[int_TargetDayId]['name_ja'] }}の束&nbsp;|&nbsp;JaVocabFlushcards{% endblock %}
{% block content %}
  <div class="container">
    <div class="row pb-3 pb-md-4 pt-1 pt-md-0">
      <h1 class="col-md-8 py-0 px-3 px-md-1 m-0 fw-bold text-nowrap" style="font-family: 'Montserrat', sans-serif; font-weight: 700;">{{ lst_Days[int_TargetDayId]['name_ja'] }}の束</h1>
      <p class="col-md-4 text-end pt-2 px-3 px-md-1 mt-auto mb-0">
        <i class="bi bi-arrow-repeat"></i>
        {{ str_CreatedDate }}
      </p>
    </div>
  </div>
  {% for dct_card in lst_Cards %}
  <section class="bg-secondary my-2 border-0 rounded-4 p-3 px-md-4" >
    <a class="text-reset text-decoration-none px-0" data-bs-toggle="collapse" href="#card{{ dct_card['number'] }}" role="button" aria-expanded="false" aria-controls="card{{ dct_card['number'] }}">
      <div class="container px-0 pt-0 pb-2">
        <div class="d-flex justify-content-between">
          <div class="fs-6 px-1 border border-light border-1 rounded-2 my-auto">{{ dct_card['genre'] }}</div>
          <div class="fs-7 p-0 pe-1 lh-sm">{{ dct_card['number'] }}</div>
        </div>
      </div>
      <div class="fs-3" style="font-family: 'YakuHanMPs', 'Noto Serif JP', serif; font-weight: 400;">{{ dct_card['question'] }}</div>
    </a>

    <div class="collapse px-0 fs-3" style="font-family: 'YakuHanMPs', 'Noto Serif JP', serif; font-weight: 400;" id="card{{ dct_card['number'] }}">
      <hr class="my-2 bg-white"/>
      {{ dct_card['answer'] }}
    </div>
  </section>
  {% endfor %}
{% endblock %}