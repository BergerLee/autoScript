
const url = $request.url;
const originalBody = $response.body;

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
  },

  // 会员信息：仅修改 userVipInfo
  {
    pattern: /\/api\/strategy\/get_member_info_page(?:\?|$)/,
    handler: function (data) {
      const vip = data?.data?.userVipInfo;

      data.data.nickname = "111";

      if (!vip || typeof vip !== "object") {
        return data;
      }

      // 在这里配置希望客户端显示的会员信息
      const vipConfig = {
        entitlementKey: "bcz.app.vip.v1",
        memberLevel: vip.memberLevel,
        expireTime: 1924876800000,
        maxValue: vip.maxValue,
        currentValue: vip.currentValue
      };

      Object.assign(vip, vipConfig);

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
