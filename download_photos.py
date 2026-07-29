import urllib.request
import re
import os

output_dir = 'assets/real_photos'
os.makedirs(output_dir, exist_ok=True)

def scrape_and_download(name, baike_url, prefix):
    print(f'=== Scraping {name} Baidu Baike ===')
    try:
        req = urllib.request.Request(baike_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        resp = urllib.request.urlopen(req, timeout=30)
        html = resp.read().decode('utf-8', errors='ignore')
        
        img_urls = re.findall(r'https?://[^\"\s]+\.(?:jpg|jpeg|png|gif)[^\"\s]*', html)
        print(f'Found {len(img_urls)} image URLs')
        
        # Filter for likely portrait/photo URLs (not icons, CSS sprites, etc.)
        photo_urls = []
        for url in img_urls:
            url_lower = url.lower()
            # Skip small UI elements
            if any(x in url_lower for x in ['icon', 'logo', 'arrow', 'bg_', 'button', 'dot', 'pixel', '1x1']):
                continue
            # Skip very short URLs
            if len(url) < 50:
                continue
            photo_urls.append(url)
        
        print(f'Filtered to {len(photo_urls)} potential photos')
        for i, url in enumerate(photo_urls[:5]):
            print(f'  [{i}] {url[:150]}')
        
        # Download first few
        downloaded = 0
        for i, url in enumerate(photo_urls[:5]):
            if downloaded >= 2:  # Download max 2 per person
                break
            try:
                ext = 'jpg'
                if '.png' in url.lower():
                    ext = 'png'
                elif '.gif' in url.lower():
                    ext = 'gif'
                filename = f'{prefix}_{downloaded+1}.{ext}'
                filepath = os.path.join(output_dir, filename)
                req2 = urllib.request.Request(url, 
                    headers={'User-Agent': 'Mozilla/5.0', 'Referer': baike_url})
                with urllib.request.urlopen(req2, timeout=20) as r:
                    data = r.read()
                    if len(data) > 5000:  # > 5KB
                        with open(filepath, 'wb') as f:
                            f.write(data)
                        print(f'  DOWNLOADED: {filename} ({len(data)} bytes)')
                        downloaded += 1
                    else:
                        print(f'  SKIPPED small: {url[:80]}')
            except Exception as e:
                print(f'  FAIL: {e}')
        
        if downloaded == 0:
            print(f'  WARNING: No photos downloaded for {name}')
        return downloaded
    except Exception as e:
        print(f'Error scraping {name}: {e}')
        return 0

# Download for each master
scrape_and_download('柯俊', 'https://baike.baidu.com/item/%E6%9F%AF%E4%BF%8A/19280', 'kejun')
print()
scrape_and_download('张兴钤', 'https://baike.baidu.com/item/%E5%BC%A0%E5%85%B4%E9%92%A4/839194', 'zhangxingqian')
print()
scrape_and_download('胡赓祥', 'https://baike.baidu.com/item/%E8%83%A1%E8%B5%93%E7%A5%A5/63960764', 'hugengxiang')

print('\nDONE!')
print('\nFiles in output directory:')
for f in sorted(os.listdir(output_dir)):
    size = os.path.getsize(os.path.join(output_dir, f))
    print(f'  {f} ({size} bytes)')
