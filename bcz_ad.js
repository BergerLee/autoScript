
const url = $request.url;
const method = $request.method;
const originalBody = $response.body;

// 只在这里登记已经确认需要处理的接口
const rules = [
  {
    pattern: /\/api\/mall\/proxy\/homepage\/get_recommend_goods_by_page(?:\?|$)/,
    handler: function (data) {
      if (!data || typeof data !== "object") return data;
      if (!data.data || typeof data.data !== "object") return data;

      data.data.total = 0;
      data.data.goodsInfo = [];
      return data;
    }
  }

  // 发现新接口后，在这里继续添加规则
];

function finish(body) {
  $done({ body: body });
}

if (!originalBody || method !== "GET" && method !== "POST") {
  finish(originalBody);
} else {
  let matched = false;

  for (const rule of rules) {
    if (!rule.pattern.test(url)) continue;
    matched = true;

    try {
      const data = JSON.parse(originalBody);
      const result = rule.handler(data);
      finish(JSON.stringify(result));
    } catch (e) {
      finish(originalBody);
    }

    break;
  }

  if (!matched) finish(originalBody);
}
