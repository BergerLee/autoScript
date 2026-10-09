
const url = $request.url;

const rules = [
  // 首页推荐商品
  {
    pattern: /\/api\/mall\/proxy\/homepage\/get_recommend_goods_by_page(?:\?|$)/,
    handler: function (data) {
      if (data?.data && typeof data.data === "object") {
        data.data.total = 0;
        data.data.goodsInfo = [];
      }
      return data;
    }
  }
];

if (!originalBody) {
  $done({});
} else {
  try {
    const data = JSON.parse(originalBody);
    const matchedRule = rules.find(rule => rule.pattern.test(url));

    if (matchedRule) {
      const result = matchedRule.handler(data);
      $done({ body: JSON.stringify(result) });
    } else {
      $done({});
    }
  } catch (e) {
    $done({});
  }
}
