import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

urls = [
    'https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/server.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/MTProtoProxy/main/mtproto.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/vmess.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/vless.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub2.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Warp_sub.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/tuic.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/hysteria2.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/trojan.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/ss.txt',
    'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/ssr.txt',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/mix',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/base64/mix',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/config.txt',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/lite/subscriptions/location/normal/CA',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/lite/subscriptions/location/normal/DE',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/lite/subscriptions/xray/normal/mix',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/warp/config',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/tuic',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/hy2',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/trojan',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/ss',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/clash/vmess',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/clash/trojan',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/meta/vless',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/meta/reality',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/meta/ss',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/meta/trojan',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/meta/vmess',
    'https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/reality',
    'https://raw.githubusercontent.com/yebekhe/outline/main/collect',
    'https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vmess_iran.txt',
    'https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/vless_iran.txt',
    'https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt',
    'https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/trojan_iran.txt',
    'https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/ss_iran.txt',
    'https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet_META_IRAN-Direct.yml',
    'https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet_iOS.txt',
    'https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.json',
    'https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt',
    'https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt',
    'https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Config%20list1.txt',
    'https://raw.githubusercontent.com/Mohammadgb0078/IRV2ray/main/vless.txt',
    'https://raw.githubusercontent.com/Mohammadgb0078/IRV2ray/main/vmess.txt',
    'https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt',
    'https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v202603032',
    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt',
    'https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub',
    'https://raw.githubusercontent.com/vxiaov/free_proxies/main/links.txt',
    'https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/reality',
    'https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/subscribe/protocols/reality',
]

def check_url(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=10)
        return url, response.status, True
    except urllib.error.HTTPError as e:
        return url, e.code, False
    except urllib.error.URLError as e:
        return url, str(e), False
    except Exception as e:
        return url, str(e), False

print('开始检测订阅地址有效性...')
print('=' * 80)

valid = []
invalid = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check_url, url): url for url in urls}
    for future in as_completed(futures):
        url, status, is_valid = future.result()
        if is_valid:
            valid.append(url)
            print(f'✓ VALID: {url}')
        else:
            invalid.append((url, status))
            print(f'✗ INVALID: {url} (Status: {status})')

print('=' * 80)
print(f'\n统计结果:')
print(f'有效: {len(valid)}')
print(f'无效: {len(invalid)}')

if invalid:
    print(f'\n无效地址列表:')
    for url, status in invalid:
        print(f'  - {url} ({status})')
