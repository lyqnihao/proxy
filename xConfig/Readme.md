[xconfig](https://xconfig.pages.dev/index2)：<br>
https://raw.githubusercontent.com/lyqnihao/proxy/refs/heads/main/xConfig/output.yaml<br>
该网页有很多订阅，换一个，改为每天4:05自动更新代理列表。<br>

如果内容未更新或程序运行错误，则向xxx@163.com发送报错邮件。

### 尝试让AI对页面分析提取订阅，并检测有效性，大多AI不能完成，以下是几个完成的，结果也不一样。

#### 1、用MiniMax M2，速度较慢，获得最少<br>
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

#### 2、Grok<br>
用 15 秒超时 + 200 字节内容 + 必须含节点关键字 的严格标准，得32条存活。能识别到是订阅节点，以节点内容为标准检测。<br>

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

#### 3、腾讯元宝：混元模型无法联网检索，DeepSeek模型完成。速度快，获取最多。<br>
#	有效地址
1	 https://raw.githubusercontent.com/chinnsenn/static-files/main/u3base.json 46
2	 https://raw.githubusercontent.com/chinnsenn/static-files/main/proxy.json 46
3	 https://raw.githubusercontent.com/chinnsenn/static-files/main/ai.json 46
4	 https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/nodes.txt 
5	 https://raw.githubusercontent.com/anaer/Sub/main/config.json 
6	 https://raw.githubusercontent.com/peasoft/NoWalls/main/routes.json 
7	 https://raw.githubusercontent.com/peasoft/NoWalls/main/rules.json 
8	 https://raw.githubusercontent.com/peasoft/NoWalls/main/rulelist 
9	 https://raw.githubusercontent.com/peasoft/NoWalls/main/rule_surge.list 
10	 https://raw.githubusercontent.com/peasoft/NoWalls/main/rule_clash.list 
11	 https://raw.githubusercontent.com/peasoft/NoWalls/main/list 
12	 https://raw.githubusercontent.com/peasoft/NoWalls/main/directlist 
13	 https://raw.githubusercontent.com/peasoft/NoWalls/main/rejectlist 
14	 https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/main/sr_top500_banlist.conf 
15	 https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/main/proxy.txt 
16	 https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/main/sr_top500_whitelist.conf 
17	 https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/main/classical.txt 
18	 https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/main/weixin.txt 
19	 https://raw.githubusercontent.com/chenggwww/surge/main/ai.list 
20	 https://raw.githubusercontent.com/chenggwww/surge/main/stream.list 
21	 https://raw.githubusercontent.com/chenggwww/surge/main/global.list 
22	 https://raw.githubusercontent.com/zhangke0516/myrule/main/Clash.yaml 
23	 https://raw.githubusercontent.com/zhangke0516/myrule/main/Surge.yaml 
24	 https://raw.githubusercontent.com/zhangke0516/myrule/main/Shadow.yaml 
25	 https://raw.githubusercontent.com/zhangke0516/myrule/main/QuanX.conf 
26	 https://raw.githubusercontent.com/zhangke0516/myrule/main/Loon.conf 
27	 https://raw.githubusercontent.com/zhangke0516/myrule/main/Stash.yaml 
28	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/Shadowrocket/provider.yaml 
29	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/Clash/provider.yaml 
30	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/Surge/provider.yaml 
31	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/Stash/provider.yaml 
32	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/Loon/provider.yaml 
33	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/QuanX/provider.yaml 
34	 https://raw.githubusercontent.com/d3ck/my-rules/main/rule-set-provider/rule-providers/Sing-Box/provider.yaml 

