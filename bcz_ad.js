
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
    if (!data || typeof data !== "object") {
      return data;
    }

    // 确保 data.data 存在
    if (!data.data || typeof data.data !== "object") {
      data.data = {};
    }

    // 如果没有 userVipInfo，则自动添加
    if (
      !data.data.userVipInfo ||
      typeof data.data.userVipInfo !== "object" ||
      Array.isArray(data.data.userVipInfo)
    ) {
      data.data.userVipInfo = {};
    }

    const vip = data.data.userVipInfo;

    // 配置希望客户端显示的会员信息
    const vipConfig = {
      entitlementKey: "bcz.app.vip.v1",
      memberLevel: vip.memberLevel ?? 1,
      expireTime: 1924876800000,
      maxValue: vip.maxValue ?? 999999,
      currentValue: vip.currentValue ?? 0
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
