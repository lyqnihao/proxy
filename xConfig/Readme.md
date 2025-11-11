[xconfig](https://xconfig.pages.dev/index2)：<br>
[https://raw.githubusercontent.com/lyqnihao/proxy/refs/heads/main/xConfig/output.yaml](https://raw.githubusercontent.com/lyqnihao/proxy/refs/heads/main/xConfig/output.yaml?token=GHSAT0AAAAAADLQZNYIVIQAQQZ6WCQ6KJLC2IREACA)<br>
该网页有很多订阅，换一个，改为每天4:05自动更新代理列表。<br>

如果内容未更新或程序运行错误，则向xxx@163.com发送报错邮件。

### 尝试让AI对页面分析提取订阅，并检测有效性，大多AI不能完成，以下是几个完成的，结果也不一样。

#### 1、用MiniMax M2<br>
速度较慢，获得最少<br>
检测结果：<br>
提取总数: 55个URL<br>
有效URL: 19个<br>
无效URL: 36个<br>
无效原因统计：<br>
HTTP 404错误: 26个 (文件不存在)<br>
连接超时: 6个 (网络问题)<br>
连接错误: 4个 (无法访问)<br>
有效的19个URL：<br>
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vless_iran.txt
https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt
https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt
https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/server.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vmess_iran.txt
https://raw.githubusercontent.com/vxiaov/free_proxies/main/links.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt
https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt
https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub
https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt
https://raw.githubusercontent.com/Mohammadgb0078/IRV2ray/main/vless.txt
https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt
https://raw.githubusercontent.com/ALIILAPRO/MTProtoProxy/main/mtproto.txt
https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt
https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt
https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2
https://raw.githubusercontent.com/Mohammadgb0078/IRV2ray/main/vmess.txt
https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.json
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/trojan_iran.txt

#### 2、Grok：
用 15 秒超时 + 200 字节内容 + 必须含节点关键字 的严格标准，得32条存活。能识别到是订阅节点，以节点内容为标准检测。虽然Grok一再保证它验证了以下所有订阅都有效，可复制出来很地址明显被“u3base”这个特殊字段污染，所剩有效地址不多。<br>

https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/u3base.txt
https://raw.githubusercontent.com/ermaozi/adblock/main/u3base.txt
https://raw.githubusercontent.com/peasoft/NoLanzhu/main/u3base.txt
https://raw.githubusercontent.com/427ru-r/PRO/main/u3base.txt
https://raw.githubusercontent.com/chfchf0306/clash/main/u3base.yml
https://raw.githubusercontent.com/mfuu/u3/base.yml
https://raw.githubusercontent.com/shoujiyanxishe/atu/main/u3base.yaml
https://raw.githubusercontent.com/frainsAi/Flik/u3base.yaml
https://raw.githubusercontent.com/fi25/Clash/main/u3base.yaml
https://raw.githubusercontent.com/Hackl0us/SS-Rule-Snippet/master/LAZY_RULES/u3base.yaml
https://raw.githubusercontent.com/SnapdragonLee/SystemProxy/master/dist/u3base.yaml
https://raw.githubusercontent.com/Moli-X/Resources/main/Clash/u3base.yaml
https://raw.githubusercontent.com/Toperlock/clash/main/u3base.yaml
https://raw.githubusercontent.com/wanglin-1/u3/master/u3base.yaml
https://raw.githubusercontent.com/sun9426/sun9426.github.io/main/Clash/u3base.yaml
https://raw.githubusercontent.com/ts-sf/Clash/main/Base/u3base.yaml
https://raw.githubusercontent.com/alanbobs999/TopFreeProxies/master/sub/u3base.txt
https://raw.githubusercontent.com/adiwzx/freenode/main/adispeed.yml
https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.txt
https://raw.githubusercontent.com/ripaojiedian/freenode/main/u3base.txt
https://raw.githubusercontent.com/Pawdroid/Free-servers/main/u3base.txt
https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub/u3base.txt
https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity.yml
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vless_iran.txt
https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt
https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vmess_iran.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt
https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt
https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt
https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/trojan_iran.txt

#### 3、腾讯元宝：
混元模型无法联网检索，DeepSeek模型完成。速度快，获取最多，但有效性检测能力极差。<br>


#### 4、Kimi的 OK computer：
也很不错，结果效果第二好，就是有点慢。<br>
📊 提取结果概览<br>
总链接数：55个<br>
有效链接：22个（40%成功率）<br>
无效链接：33个（多为404错误）<br>
✅ 验证标准<br>
采用三重验证机制：<br>
1. 状态码200验证<br>
2. 内容非空检测<br>
3. 响应时间<5秒<br>

https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt
https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/server.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vmess_iran.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vless_iran.txt
https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt
https://raw.githubusercontent.com/Mohammadgb0078/IRV2ray/main/vless.txt
https://raw.githubusercontent.com/Mohammadgb0078/IRV2ray/main/vmess.txt
https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt
https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt
https://raw.githubusercontent.com/vxiaov/free_proxies/main/links.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt
https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2
https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub
https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt
https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet_iOS.txt
https://raw.githubusercontent.com/ALIILAPRO/MTProtoProxy/main/mtproto.txt
https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt
https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt
https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/trojan_iran.txt
https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.json
https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/ss_iran.txt