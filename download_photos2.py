import urllib.request
import re
import os

output_dir = 'assets/real_photos'
os.makedirs(output_dir, exist_ok=True)

def fetch_page(url, referer=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    if referer:
        headers['Referer'] = referer
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.read().decode('utf-8', errors='ignore')

def extract_and_download(html, prefix, max_count=2):
    # Find all img URLs
    img_urls = re.findall(r'(?:src|data-src)=["\']([^"\']+\.(?:jpg|jpeg|png))["\']', html)
    # Also try other patterns
    if not img_urls:
        img_urls = re.findall(r'https?://[^\"\s<>]+\.(?:jpg|jpeg|png)[^\"\s<>]*', html)
    
    # Convert relative to absolute
    absolute_urls = []
    for url in img_urls:
        if url.startswith('//'):
            url = 'https:' + url
        elif not url.startswith('http'):
            continue
        absolute_urls.append(url)
    
    # Filter out small UI images
    photo_urls = []
    for url in absolute_urls:
        url_lower = url.lower()
        if any(x in url_lower for x in ['icon', 'logo', 'avatar_small', 'emoji', 'pixel', '1x1', 'statistic']):
            continue
        photo_urls.append(url)
    
    print(f'Found {len(photo_urls)} potential photos')
    
    downloaded = 0
    for url in photo_urls:
        if downloaded >= max_count:
            break
        try:
            ext = 'jpg'
            if '.png' in url.lower():
                ext = 'png'
            filename = f'{prefix}_{downloaded+1}.{ext}'
            filepath = os.path.join(output_dir, filename)
            
            req = urllib.request.Request(url, 
                headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.toutiao.com/'})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
                if len(data) > 10000:  # > 10KB for real photos
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f'  OK: {filename} ({len(data)} bytes) <- {url[:100]}')
                    downloaded += 1
                else:
                    print(f'  SKIP: too small ({len(data)} bytes): {url[:80]}')
        except Exception as e:
            print(f'  FAIL: {e}')
    
    return downloaded

# Try toutiao for 柯俊
print('=== 柯俊 from toutiao ===')
try:
    html = fetch_page('https://www.toutiao.com/article/6454679135909315086/')
    extract_and_download(html, 'kejun', 2)
except Exception as e:
    print(f'Error: {e}')

print()
print('=== 张兴钤 from CAST ===')
try:
    html = fetch_page('https://mmcs.cast.org.cn/gzb/rwbd/zxxx/art/2023/art_e6f5af6bd74c4375b55f8329ae5b3d4d.html')
    extract_and_download(html, 'zhangxingqian', 2)
except Exception as e:
    print(f'Error: {e}')

print()
print('=== 张兴钤 from toutiao ===')
try:
    html = fetch_page('https://www.toutiao.com/article/7019592681110159883/')
    extract_and_download(html, 'zhangxingqian_a', 2)
except Exception as e:
    print(f'Error: {e}')

print()
print('=== Checking photos ===')
for f in sorted(os.listdir(output_dir)):
    size = os.path.getsize(os.path.join(output_dir, f))
    print(f'  {f} ({size} bytes)')
