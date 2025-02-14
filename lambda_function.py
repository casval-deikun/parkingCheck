import json

# ---------------------------
# 1) manifest.json 내용
# ---------------------------
MANIFEST_JSON = r"""{
    "name": "성균관대 1공학관 주차",
    "start_url": "/",
    "display": "fullscreen",
    "short_name": "성대 1공 주차",
    "id": "risefreeparking",
    "description": "made by Leeusihoon",
    "icons": [
      {
        "src": "https://blog.kakaocdn.net/dn/E8h6W/btsLXRcwIlg/n2YkaDrXZgkLm1pr2F12k0/img.png",
        "type": "image/png",
        "sizes": "192x192"
      },
      {
        "src": "https://blog.kakaocdn.net/dn/boBZzT/btsLXR4FXHz/B0L6PTFQr2v9jdqmAjKhFK/img.png",
        "type": "image/png",
        "sizes": "512x512"
      }
    ]
}"""

# ---------------------------
# 2) service-worker.js 내용 (기본적인 오프라인 캐싱 예시)
# ---------------------------
SERVICE_WORKER_JS = r"""console.log('[Service Worker] Loaded');

const CACHE_NAME = 'my-pwa-cache-v1.1';
const INITIAL_CACHE_URLS = [
  '/',             // index.html
  '/manifest.json' // manifest
];

// 설치 시 미리 캐시
self.addEventListener('install', (event) => {
  console.log('[SW] Install event');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching initial files');
      return cache.addAll(INITIAL_CACHE_URLS);
    })
  );
});

// 활성화 시 오래된 캐시 정리
self.addEventListener('activate', (event) => {
  console.log('[SW] Activate event');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(name => {
          if (name !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          }
        })
      );
    })
  );
});
// fetch 이벤트 (캐시 우선 로직)
// fetch 이벤트
self.addEventListener('fetch', (event) => {
  const reqUrl = new URL(event.request.url);

  // 1) /get-button-status 등의 동적 요청인지 체크
  if (reqUrl.pathname === '/get-button-status') {
    // --> 네트워크 우선 (fetch) 하고, 실패 시 캐시(오프라인) 처리 등
    event.respondWith(
      fetch(event.request).catch(err => {
        console.error('[SW] Fetch failed:', err);
        return new Response("오프라인 상태", { status: 503 });
      })
    );
  }
  // 2) 그 외 (정적 파일 등)만 기존처럼 캐시 우선
  else {
    event.respondWith(
      caches.match(event.request).then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(networkResponse => {
          // 받은 정적 파일은 캐시에 저장
          ...
        });
      })
    );
  }
});
"""
# ---------------------------
# 3) HTML (메인 페이지)
# ---------------------------
HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=9800">
    <title>제1 공학관 주차 체크</title>

    <!-- manifest.json 연결 (상대경로 /manifest.json) -->
    <link rel="manifest" href="/manifest.json" />
    <meta name="theme-color" content="#ffffff" />

    <!-- 아이콘 -->
    <link rel="icon" href="https://blog.kakaocdn.net/dn/E8h6W/btsLXRcwIlg/n2YkaDrXZgkLm1pr2F12k0/img.png" />
    <link rel="icon" href="https://blog.kakaocdn.net/dn/boBZzT/btsLXR4FXHz/B0L6PTFQr2v9jdqmAjKhFK/img.png" />

    <style>
        .container {
            transform: scale(0.83); 
            transform-origin: top left;
            position: relative;
            width: 9800px;
            height: 18600px;
            background-color: white;
            border: 1px solid black;
            overflow: hidden;
        }
        .space {
            position: absolute;
            border: 2px solid black;
            text-align: center;
            line-height: normal;
            cursor: pointer;
            font-size: 65px
        }
        .navigation button {
            border: 8px solid black;
            text-align: center;
            line-height: normal;
            cursor: pointer;
            font-size: 100px;
        }  
        .navigation button:hover {
            background-color: #ff6347;
            transform: scale(1.1);
        }
        .gate {
            position: absolute;
            border: 2px solid black;
            text-align: center;
            line-height: normal;
            cursor: pointer;
            font-size: 200px;
            color : #d8cccf;
            background-color: #3c2529;
            
        }
        body {
            transform: scale(0.183);
            transform-origin: top left;
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #fff7e6, #ffdab9);
        }
    </style>

    <script>
      // 서비스 워커 등록
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
          .then(reg => console.log('Service Worker 등록 성공!', reg))
          .catch(err => console.error('SW 등록 실패:', err));
      }
    </script>
</head>
<body>
    <div class="navigation" style="top: 750px; left: 500px; width: 2000px; height: 500px;">
        <button onclick="showPage(1)" class="button-1" style="background-color: yellow; top: 750px; left: 100px; width: 600px; height: 300px;">좌측 구역</button>
        <button onclick="showPage(2)" class="button-2" style="background-color: red; top: 750px; left: 500px; width: 600px; height: 300px;">중간 구역</button>
        <button onclick="showPage(3)" class="button-3" style="background-color: greenyellow; top: 750px; left: 900px; width: 600px; height: 300px;">우측 구역</button>
        <img src="https://blog.kakaocdn.net/dn/6jipq/btsL5rpPSmw/jGKhBz1DQqbZu2K1KGJo51/img.png"
         alt="My Image"
         style="
             position: absolute;
             top: 10px;  /* 버튼들과 맞춰보세요 */
             left: 1830px; /* 버튼들 옆에 배치할 x좌표 */
             width: 1000px;
             height: 900px; 
             z-index: 9999
            " />
        <div style="
        position: absolute;
        top: 10px;         /* 이미지 하단(900px)보다 200px 정도 아래 */
        left: 2950px;        /* 이미지는 left:1830 ~ 2830까지 차지 → 120px 정도 오른쪽 여유 */
        width: 1500px;        
        padding: 20px;
        background-color: #f8f8f8;
        border: 3px solid #333;
        border-radius: 10px;
        z-index: 9999;
        font-size: 100px;
        line-height: 1.2;
      ">
        <p style="margin: 10px 0;">
          <span style=" display:inline-block; width:200px; height:150px; background-color:red; vertical-align:middle; margin-right:10px;"></span>
          주차됨
        </p>
        <p style="margin: 10px 0;">
          <span style=" display:inline-block; width:200px; height:150px; background-color:greenyellow; vertical-align:middle; margin-right:10px;"></span>
          비어있음
        </p>
        <p style="margin: 10px 0;">
          <span style=" display:inline-block; width:200px; height:150px; background-color:orange; vertical-align:middle; margin-right:10px;"></span>
          장애인 주차구역
        </p>
        <div id="zone-info" style="
         position: absolute;
         top: 10px;  /* 버튼들 아래에 적절히 배치 예시 */
         left: 2000px;
         width: 800px;
         height: 500px;
         background-color: #ffffff;
         border: 5px solid #333;
         padding: 20px;
         border-radius: 10px;
         z-index: 9999;
         font-size: 62px;">
      <div id="zone1-info"></div>
      <div id="zone2-info" style="margin-top:40px;"></div>
      <div id="zone3-info" style="margin-top:40px;"></div>
    </div>
      </div>
    </div>
    <div class="container" id="page1">
        <div class="space" style="top: 120px; left: 120px; width: 1440px; height: 420px;">Button 1</div>
        <div class="space" style="top: 120px; left: 3880px; width: 400px; height: 700px;">Button 2</div>
        <div class="space" style="top: 120px; left: 4340px; width: 420px; height: 700px;">Button 3</div>
        <div class="space" style="top: 120px; left: 4820px; width: 400px; height: 700px;">Button 4</div>
        <div class="space" style="top: 120px; left: 5300px; width: 400px; height: 700px;">Button 5</div>
        <div class="space" style="top: 120px; left: 5760px; width: 420px; height: 700px;">Button 6</div>
        <div class="space" style="top: 120px; left: 6220px; width: 420px; height: 700px;">Button 7</div>
        <div class="space" style="top: 120px; left: 6700px; width: 420px; height: 700px;">Button 8</div>
        <div class="space" style="top: 120px; left: 7180px; width: 400px; height: 700px;">Button 9</div>
        <div class="space" style="top: 120px; left: 7640px; width: 420px; height: 700px;">Button 10</div>
        <div class="space" style="top: 120px; left: 8120px; width: 420px; height: 700px;">Button 11</div>
        <div class="space" style="top: 120px; left: 8580px; width: 420px; height: 700px;">Button 12</div>
        <div class="space" style="top: 120px; left: 9060px; width: 420px; height: 700px;">Button 13</div>
        <div class="space" style="top: 600px; left: 120px; width: 1440px; height: 440px;">Button 14</div>
        <div class="space" style="top: 1080px; left: 120px; width: 1440px; height: 440px;">Button 15</div>
        <div class="space" style="top: 1540px; left: 2040px; width: 540px; height: 220px;">Button 16</div>
        <div class="space" style="top: 1540px; left: 2640px; width: 340px; height: 640px;">Button 17</div>
        <div class="space" style="top: 1540px; left: 3020px; width: 360px; height: 640px;">Button 18</div>
        <div class="space" style="top: 1540px; left: 3420px; width: 340px; height: 640px;">Button 19</div>
        <div class="space" style="top: 1540px; left: 3820px; width: 320px; height: 640px;">Button 20</div>
        <div class="space" style="top: 1540px; left: 4200px; width: 340px; height: 640px;">Button 21</div>
        <div class="space" style="top: 1540px; left: 4600px; width: 320px; height: 640px;">Button 22</div>
        <div class="space" style="top: 1540px; left: 4980px; width: 340px; height: 640px;">Button 23</div>
        <div class="space" style="top: 1540px; left: 5380px; width: 340px; height: 640px;">Button 24</div>
        <div class="space" style="top: 1540px; left: 5780px; width: 320px; height: 640px;">Button 25</div>
        <div class="space" style="top: 1540px; left: 6160px; width: 340px; height: 640px;">Button 26</div>
        <div class="space" style="top: 1540px; left: 6540px; width: 360px; height: 640px;">Button 27</div>
        <div class="space" style="top: 1540px; left: 6940px; width: 340px; height: 640px;">Button 28</div>
        <div class="space" style="top: 1540px; left: 7340px; width: 320px; height: 640px;">Button 29</div>
        <div class="space" style="top: 1540px; left: 7720px; width: 340px; height: 640px;">Button 30</div>
        <div class="space" style="top: 1540px; left: 8120px; width: 320px; height: 640px;">Button 31</div>
        <div class="space" style="top: 1540px; left: 8520px; width: 320px; height: 640px;">Button 32</div>
        <div class="space" style="top: 1540px; left: 8900px; width: 340px; height: 640px;">Button 33</div>
        <div class="space" style="top: 1580px; left: 120px; width: 1440px; height: 420px;">Button 34</div>
        <div class="space" style="top: 1820px; left: 2040px; width: 540px; height: 220px;">Button 35</div>
        <div class="space" style="top: 2100px; left: 2040px; width: 540px; height: 220px;">Button 36</div>
        <div class="space" style="top: 2240px; left: 2640px; width: 340px; height: 640px;">Button 37</div>
        <div class="space" style="top: 2240px; left: 3020px; width: 360px; height: 640px;">Button 38</div>
        <div class="space" style="top: 2240px; left: 3420px; width: 340px; height: 640px;">Button 39</div>
        <div class="space" style="top: 2240px; left: 3820px; width: 320px; height: 640px;">Button 40</div>
        <div class="space" style="top: 2240px; left: 4200px; width: 340px; height: 640px;">Button 41</div>
        <div class="space" style="top: 2240px; left: 4600px; width: 320px; height: 640px;">Button 42</div>
        <div class="space" style="top: 2240px; left: 4980px; width: 340px; height: 640px;">Button 43</div>
        <div class="space" style="top: 2240px; left: 5380px; width: 340px; height: 640px;">Button 44</div>
        <div class="space" style="top: 2240px; left: 5780px; width: 320px; height: 640px;">Button 45</div>
        <div class="space" style="top: 2240px; left: 6160px; width: 340px; height: 640px;">Button 46</div>
        <div class="space" style="top: 2240px; left: 6540px; width: 360px; height: 640px;">Button 47</div>
        <div class="space" style="top: 2240px; left: 6940px; width: 340px; height: 640px;">Button 48</div>
        <div class="space" style="top: 2240px; left: 7340px; width: 320px; height: 640px;">Button 49</div>
        <div class="space" style="top: 2240px; left: 7720px; width: 340px; height: 640px;">Button 50</div>
        <div class="space" style="top: 2240px; left: 8120px; width: 320px; height: 640px;">Button 51</div>
        <div class="space" style="top: 2240px; left: 8520px; width: 320px; height: 640px;">Button 52</div>
        <div class="space" style="top: 2240px; left: 8900px; width: 340px; height: 640px;">Button 53</div>
        <div class="space" style="top: 2380px; left: 2040px; width: 540px; height: 220px;">Button 54</div>
        <div class="space" style="top: 2660px; left: 2040px; width: 540px; height: 220px;">Button 55</div>
        <div class="space" style="top: 3340px; left: 2040px; width: 540px; height: 240px;">Button 56</div>
        <div class="space" style="top: 3340px; left: 2640px; width: 340px; height: 660px;">Button 57</div>
        <div class="space" style="top: 3340px; left: 3020px; width: 360px; height: 660px;">Button 58</div>
        <div class="space" style="top: 3340px; left: 3420px; width: 340px; height: 660px;">Button 59</div>
        <div class="space" style="top: 3340px; left: 3820px; width: 320px; height: 660px;">Button 60</div>
        <div class="space" style="top: 3340px; left: 4200px; width: 340px; height: 660px;">Button 61</div>
        <div class="space" style="top: 3340px; left: 4600px; width: 320px; height: 660px;">Button 62</div>
        <div class="space" style="top: 3340px; left: 4980px; width: 340px; height: 660px;">Button 63</div>
        <div class="space" style="top: 3340px; left: 5380px; width: 340px; height: 660px;">Button 64</div>
        <div class="space" style="top: 3340px; left: 5780px; width: 320px; height: 660px;">Button 65</div>
        <div class="space" style="top: 3340px; left: 6160px; width: 340px; height: 660px;">Button 66</div>
        <div class="space" style="top: 3340px; left: 6540px; width: 360px; height: 660px;">Button 67</div>
        <div class="space" style="top: 3340px; left: 6940px; width: 340px; height: 660px;">Button 68</div>
        <div class="space" style="top: 3340px; left: 7340px; width: 320px; height: 660px;">Button 69</div>
        <div class="space" style="top: 3340px; left: 7720px; width: 340px; height: 660px;">Button 70</div>
        <div class="space" style="top: 3340px; left: 8120px; width: 320px; height: 660px;">Button 71</div>
        <div class="space" style="top: 3340px; left: 8520px; width: 320px; height: 660px;">Button 72</div>
        <div class="space" style="top: 3340px; left: 8900px; width: 340px; height: 660px;">Button 73</div>
        <div class="space" style="top: 3620px; left: 2040px; width: 540px; height: 240px;">Button 74</div>
        <div class="space" style="top: 3900px; left: 2040px; width: 540px; height: 240px;">Button 75</div>
        <div class="space" style="top: 4040px; left: 2640px; width: 340px; height: 660px;">Button 76</div>
        <div class="space" style="top: 4040px; left: 3020px; width: 360px; height: 660px;">Button 77</div>
        <div class="space" style="top: 4040px; left: 3420px; width: 340px; height: 660px;">Button 78</div>
        <div class="space" style="top: 4040px; left: 3820px; width: 320px; height: 660px;">Button 79</div>
        <div class="space" style="top: 4040px; left: 4200px; width: 340px; height: 660px;">Button 80</div>
        <div class="space" style="top: 4040px; left: 4600px; width: 320px; height: 660px;">Button 81</div>
        <div class="space" style="top: 4040px; left: 4980px; width: 340px; height: 660px;">Button 82</div>
        <div class="space" style="top: 4040px; left: 5380px; width: 340px; height: 660px;">Button 83</div>
        <div class="space" style="top: 4040px; left: 5780px; width: 320px; height: 660px;">Button 84</div>
        <div class="space" style="top: 4040px; left: 6160px; width: 340px; height: 660px;">Button 85</div>
        <div class="space" style="top: 4040px; left: 6540px; width: 360px; height: 660px;">Button 86</div>
        <div class="space" style="top: 4040px; left: 6940px; width: 340px; height: 660px;">Button 87</div>
        <div class="space" style="top: 4040px; left: 7340px; width: 320px; height: 660px;">Button 88</div>
        <div class="space" style="top: 4040px; left: 7720px; width: 340px; height: 660px;">Button 89</div>
        <div class="space" style="top: 4040px; left: 8120px; width: 320px; height: 660px;">Button 90</div>
        <div class="space" style="top: 4040px; left: 8520px; width: 320px; height: 660px;">Button 91</div>
        <div class="space" style="top: 4040px; left: 8900px; width: 340px; height: 660px;">Button 92</div>
        <div class="space" style="top: 4180px; left: 2040px; width: 540px; height: 240px;">Button 93</div>
        <div class="space" style="top: 4460px; left: 2040px; width: 540px; height: 240px;">Button 94</div>
        <div class="space" style="top: 4980px; left: 2040px; width: 540px; height: 240px;">Button 95</div>
        <div class="space" style="top: 4980px; left: 2640px; width: 340px; height: 660px;">Button 96</div>
        <div class="space" style="top: 4980px; left: 3020px; width: 360px; height: 660px;">Button 97</div>
        <div class="space" style="top: 4980px; left: 3420px; width: 340px; height: 660px;">Button 98</div>
        <div class="space" style="top: 4980px; left: 3820px; width: 320px; height: 660px;">Button 99</div>
        <div class="space" style="top: 4980px; left: 4200px; width: 340px; height: 660px;">Button 100</div>
        <div class="space" style="top: 4980px; left: 4600px; width: 320px; height: 660px;">Button 101</div>
        <div class="space" style="top: 4980px; left: 4980px; width: 340px; height: 660px;">Button 102</div>
        <div class="space" style="top: 4980px; left: 5380px; width: 340px; height: 660px;">Button 103</div>
        <div class="space" style="top: 4980px; left: 5780px; width: 320px; height: 660px;">Button 104</div>
        <div class="space" style="top: 4980px; left: 6160px; width: 340px; height: 660px;">Button 105</div>
        <div class="space" style="top: 4980px; left: 6540px; width: 360px; height: 660px;">Button 106</div>
        <div class="space" style="top: 4980px; left: 6940px; width: 340px; height: 660px;">Button 107</div>
        <div class="space" style="top: 4980px; left: 7340px; width: 320px; height: 660px;">Button 108</div>
        <div class="space" style="top: 4980px; left: 7720px; width: 340px; height: 660px;">Button 109</div>
        <div class="space" style="top: 4980px; left: 8120px; width: 320px; height: 660px;">Button 110</div>
        <div class="space" style="top: 4980px; left: 8520px; width: 320px; height: 660px;">Button 111</div>
        <div class="space" style="top: 4980px; left: 8900px; width: 340px; height: 660px;">Button 112</div>
        <div class="space" style="top: 5260px; left: 2040px; width: 540px; height: 240px;">Button 113</div>
        <div class="space" style="top: 5540px; left: 2040px; width: 540px; height: 240px;">Button 114</div>
        <div class="space" style="top: 5680px; left: 2640px; width: 340px; height: 660px;">Button 115</div>
        <div class="space" style="top: 5680px; left: 3020px; width: 360px; height: 660px;">Button 116</div>
        <div class="space" style="top: 5680px; left: 3420px; width: 340px; height: 660px;">Button 117</div>
        <div class="space" style="top: 5680px; left: 3820px; width: 320px; height: 660px;">Button 118</div>
        <div class="space" style="top: 5680px; left: 4200px; width: 340px; height: 660px;">Button 119</div>
        <div class="space" style="top: 5680px; left: 4600px; width: 320px; height: 660px;">Button 120</div>
        <div class="space" style="top: 5680px; left: 4980px; width: 340px; height: 660px;">Button 121</div>
        <div class="space" style="top: 5680px; left: 5380px; width: 340px; height: 660px;">Button 122</div>
        <div class="space" style="top: 5680px; left: 5780px; width: 320px; height: 660px;">Button 123</div>
        <div class="space" style="top: 5680px; left: 6160px; width: 340px; height: 660px;">Button 124</div>
        <div class="space" style="top: 5680px; left: 6540px; width: 360px; height: 660px;">Button 125</div>
        <div class="space" style="top: 5680px; left: 6940px; width: 340px; height: 660px;">Button 126</div>
        <div class="space" style="top: 5680px; left: 7340px; width: 320px; height: 660px;">Button 127</div>
        <div class="space" style="top: 5680px; left: 7720px; width: 340px; height: 660px;">Button 128</div>
        <div class="space" style="top: 5680px; left: 8120px; width: 320px; height: 660px;">Button 129</div>
        <div class="space" style="top: 5680px; left: 8520px; width: 320px; height: 660px;">Button 130</div>
        <div class="space" style="top: 5680px; left: 8900px; width: 340px; height: 660px;">Button 131</div>
        <div class="space" style="top: 5820px; left: 2040px; width: 540px; height: 240px;">Button 132</div>
        <div class="space" style="top: 6100px; left: 2040px; width: 540px; height: 240px;">Button 133</div>
        <div class="space" style="top: 6840px; left: 2040px; width: 540px; height: 220px;">Button 134</div>
        <div class="space" style="top: 6840px; left: 2640px; width: 340px; height: 640px;">Button 135</div>
        <div class="space" style="top: 6840px; left: 3020px; width: 360px; height: 640px;">Button 136</div>
        <div class="space" style="top: 6840px; left: 3420px; width: 340px; height: 640px;">Button 137</div>
        <div class="space" style="top: 6840px; left: 3820px; width: 320px; height: 640px;">Button 138</div>
        <div class="space" style="top: 6840px; left: 4200px; width: 340px; height: 640px;">Button 139</div>
        <div class="space" style="top: 6840px; left: 4600px; width: 320px; height: 640px;">Button 140</div>
        <div class="space" style="top: 6840px; left: 4980px; width: 340px; height: 640px;">Button 141</div>
        <div class="space" style="top: 6840px; left: 5380px; width: 340px; height: 640px;">Button 142</div>
        <div class="space" style="top: 6840px; left: 5780px; width: 320px; height: 640px;">Button 143</div>
        <div class="space" style="top: 6840px; left: 6160px; width: 340px; height: 640px;">Button 144</div>
        <div class="space" style="top: 6840px; left: 6540px; width: 360px; height: 640px;">Button 145</div>
        <div class="space" style="top: 6840px; left: 6940px; width: 340px; height: 640px;">Button 146</div>
        <div class="space" style="top: 6840px; left: 7340px; width: 320px; height: 640px;">Button 147</div>
        <div class="space" style="top: 6840px; left: 7720px; width: 340px; height: 640px;">Button 148</div>
        <div class="space" style="top: 6840px; left: 8120px; width: 320px; height: 640px;">Button 149</div>
        <div class="space" style="top: 6840px; left: 8520px; width: 320px; height: 640px;">Button 150</div>
        <div class="space" style="top: 6840px; left: 8900px; width: 340px; height: 640px;">Button 151</div>
        <div class="space" style="top: 7120px; left: 2040px; width: 540px; height: 220px;">Button 152</div>
        <div class="space" style="top: 7400px; left: 2040px; width: 540px; height: 220px;">Button 153</div>
        <div class="space" style="top: 7540px; left: 2640px; width: 340px; height: 640px;">Button 154</div>
        <div class="space" style="top: 7540px; left: 3020px; width: 360px; height: 640px;">Button 155</div>
        <div class="space" style="top: 7540px; left: 3420px; width: 340px; height: 640px;">Button 156</div>
        <div class="space" style="top: 7540px; left: 3820px; width: 320px; height: 640px;">Button 157</div>
        <div class="space" style="top: 7540px; left: 4200px; width: 340px; height: 640px;">Button 158</div>
        <div class="space" style="top: 7540px; left: 4600px; width: 320px; height: 640px;">Button 159</div>
        <div class="space" style="top: 7540px; left: 4980px; width: 340px; height: 640px;">Button 160</div>
        <div class="space" style="top: 7540px; left: 5380px; width: 340px; height: 640px;">Button 161</div>
        <div class="space" style="top: 7540px; left: 5780px; width: 320px; height: 640px;">Button 162</div>
        <div class="space" style="top: 7540px; left: 6160px; width: 340px; height: 640px;">Button 163</div>
        <div class="space" style="top: 7540px; left: 6540px; width: 360px; height: 640px;">Button 164</div>
        <div class="space" style="top: 7540px; left: 6940px; width: 340px; height: 640px;">Button 165</div>
        <div class="space" style="top: 7540px; left: 7340px; width: 320px; height: 640px;">Button 166</div>
        <div class="space" style="top: 7540px; left: 7720px; width: 340px; height: 640px;">Button 167</div>
        <div class="space" style="top: 7540px; left: 8120px; width: 320px; height: 640px;">Button 168</div>
        <div class="space" style="top: 7540px; left: 8520px; width: 320px; height: 640px;">Button 169</div>
        <div class="space" style="top: 7540px; left: 8900px; width: 340px; height: 640px;">Button 170</div>
        <div class="space" style="top: 7680px; left: 2040px; width: 540px; height: 220px;">Button 171</div>
        <div class="space" style="top: 7960px; left: 2040px; width: 540px; height: 220px;">Button 172</div>
        <div class="space" style="top: 8800px; left: 2040px; width: 540px; height: 220px;">Button 173</div>
        <div class="space" style="top: 8800px; left: 2640px; width: 340px; height: 640px;">Button 174</div>
        <div class="space" style="top: 8800px; left: 3020px; width: 360px; height: 640px;">Button 175</div>
        <div class="space" style="top: 8800px; left: 3420px; width: 340px; height: 640px;">Button 176</div>
        <div class="space" style="top: 8800px; left: 3820px; width: 320px; height: 640px;">Button 177</div>
        <div class="space" style="top: 8800px; left: 4200px; width: 340px; height: 640px;">Button 178</div>
        <div class="space" style="top: 8800px; left: 4600px; width: 320px; height: 640px;">Button 179</div>
        <div class="space" style="top: 8800px; left: 4980px; width: 340px; height: 640px;">Button 180</div>
        <div class="space" style="top: 8800px; left: 5380px; width: 340px; height: 640px;">Button 181</div>
        <div class="space" style="top: 8800px; left: 5780px; width: 320px; height: 640px;">Button 182</div>
        <div class="space" style="top: 8800px; left: 6160px; width: 340px; height: 640px;">Button 183</div>
        <div class="space" style="top: 8800px; left: 6540px; width: 360px; height: 640px;">Button 184</div>
        <div class="space" style="top: 8800px; left: 6940px; width: 340px; height: 640px;">Button 185</div>
        <div class="space" style="top: 8800px; left: 7340px; width: 320px; height: 640px;">Button 186</div>
        <div class="space" style="top: 8800px; left: 7720px; width: 340px; height: 640px;">Button 187</div>
        <div class="space" style="top: 8800px; left: 8120px; width: 320px; height: 640px;">Button 188</div>
        <div class="space" style="top: 8800px; left: 8520px; width: 320px; height: 640px;">Button 189</div>
        <div class="space" style="top: 8800px; left: 8900px; width: 340px; height: 640px;">Button 190</div>
        <div class="space" style="top: 9080px; left: 2040px; width: 540px; height: 220px;">Button 191</div>
        <div class="space" style="top: 9360px; left: 2040px; width: 540px; height: 220px;">Button 192</div>
        <div class="space" style="top: 9500px; left: 2640px; width: 340px; height: 640px;">Button 193</div>
        <div class="space" style="top: 9500px; left: 3020px; width: 360px; height: 640px;">Button 194</div>
        <div class="space" style="top: 9500px; left: 3420px; width: 340px; height: 640px;">Button 195</div>
        <div class="space" style="top: 9500px; left: 3820px; width: 320px; height: 640px;">Button 196</div>
        <div class="space" style="top: 9500px; left: 4200px; width: 340px; height: 640px;">Button 197</div>
        <div class="space" style="top: 9500px; left: 4600px; width: 320px; height: 640px;">Button 198</div>
        <div class="space" style="top: 9500px; left: 4980px; width: 340px; height: 640px;">Button 199</div>
        <div class="space" style="top: 9500px; left: 5380px; width: 340px; height: 640px;">Button 200</div>
        <div class="space" style="top: 9500px; left: 5780px; width: 320px; height: 640px;">Button 201</div>
        <div class="space" style="top: 9500px; left: 6160px; width: 340px; height: 640px;">Button 202</div>
        <div class="space" style="top: 9500px; left: 6540px; width: 360px; height: 640px;">Button 203</div>
        <div class="space" style="top: 9500px; left: 6940px; width: 340px; height: 640px;">Button 204</div>
        <div class="space" style="top: 9500px; left: 7340px; width: 320px; height: 640px;">Button 205</div>
        <div class="space" style="top: 9500px; left: 7720px; width: 340px; height: 640px;">Button 206</div>
        <div class="space" style="top: 9500px; left: 8120px; width: 320px; height: 640px;">Button 207</div>
        <div class="space" style="top: 9500px; left: 8520px; width: 320px; height: 640px;">Button 208</div>
        <div class="space" style="top: 9500px; left: 8900px; width: 340px; height: 640px;">Button 209</div>
        <div class="space" style="top: 9640px; left: 2040px; width: 540px; height: 220px;">Button 210</div>
        <div class="space" style="top: 9920px; left: 2040px; width: 540px; height: 220px;">Button 211</div>
        <div class="space" style="top: 10720px; left: 2040px; width: 540px; height: 220px;">Button 212</div>
        <div class="space" style="top: 10720px; left: 2640px; width: 340px; height: 640px;">Button 213</div>
        <div class="space" style="top: 10720px; left: 3020px; width: 360px; height: 640px;">Button 214</div>
        <div class="space" style="top: 10720px; left: 3420px; width: 340px; height: 640px;">Button 215</div>
        <div class="space" style="top: 10720px; left: 3820px; width: 320px; height: 640px;">Button 216</div>
        <div class="space" style="top: 10720px; left: 4200px; width: 340px; height: 640px;">Button 217</div>
        <div class="space" style="top: 10720px; left: 4600px; width: 320px; height: 640px;">Button 218</div>
        <div class="space" style="top: 10720px; left: 4980px; width: 340px; height: 640px;">Button 219</div>
        <div class="space" style="top: 10720px; left: 5380px; width: 340px; height: 640px;">Button 220</div>
        <div class="space" style="top: 10720px; left: 5780px; width: 320px; height: 640px;">Button 221</div>
        <div class="space" style="top: 10720px; left: 6160px; width: 340px; height: 640px;">Button 222</div>
        <div class="space" style="top: 10720px; left: 6540px; width: 360px; height: 640px;">Button 223</div>
        <div class="space" style="top: 10720px; left: 6940px; width: 340px; height: 640px;">Button 224</div>
        <div class="space" style="top: 10720px; left: 7340px; width: 320px; height: 640px;">Button 225</div>
        <div class="space" style="top: 10720px; left: 7720px; width: 340px; height: 640px;">Button 226</div>
        <div class="space" style="top: 10720px; left: 8120px; width: 320px; height: 640px;">Button 227</div>
        <div class="space" style="top: 10720px; left: 8520px; width: 320px; height: 640px;">Button 228</div>
        <div class="space" style="top: 10720px; left: 8900px; width: 340px; height: 640px;">Button 229</div>
        <div class="space" style="top: 11000px; left: 2040px; width: 540px; height: 220px;">Button 230</div>
        <div class="space" style="top: 11280px; left: 2040px; width: 540px; height: 220px;">Button 231</div>
        <div class="space" style="top: 11420px; left: 2640px; width: 340px; height: 640px;">Button 232</div>
        <div class="space" style="top: 11420px; left: 3020px; width: 360px; height: 640px;">Button 233</div>
        <div class="space" style="top: 11420px; left: 3420px; width: 340px; height: 640px;">Button 234</div>
        <div class="space" style="top: 11420px; left: 3820px; width: 320px; height: 640px;">Button 235</div>
        <div class="space" style="top: 11420px; left: 4200px; width: 340px; height: 640px;">Button 236</div>
        <div class="space" style="top: 11420px; left: 4600px; width: 320px; height: 640px;">Button 237</div>
        <div class="space" style="top: 11420px; left: 4980px; width: 340px; height: 640px;">Button 238</div>
        <div class="space" style="top: 11420px; left: 5380px; width: 340px; height: 640px;">Button 239</div>
        <div class="space" style="top: 11420px; left: 5780px; width: 320px; height: 640px;">Button 240</div>
        <div class="space" style="top: 11420px; left: 6160px; width: 340px; height: 640px;">Button 241</div>
        <div class="space" style="top: 11420px; left: 6540px; width: 360px; height: 640px;">Button 242</div>
        <div class="space" style="top: 11420px; left: 6940px; width: 340px; height: 640px;">Button 243</div>
        <div class="space" style="top: 11420px; left: 7340px; width: 320px; height: 640px;">Button 244</div>
        <div class="space" style="top: 11420px; left: 7720px; width: 340px; height: 640px;">Button 245</div>
        <div class="space" style="top: 11420px; left: 8120px; width: 320px; height: 640px;">Button 246</div>
        <div class="space" style="top: 11420px; left: 8520px; width: 320px; height: 640px;">Button 247</div>
        <div class="space" style="top: 11420px; left: 8900px; width: 340px; height: 640px;">Button 248</div>
        <div class="space" style="top: 11560px; left: 2040px; width: 540px; height: 220px;">Button 249</div>
        <div class="space" style="top: 11840px; left: 2040px; width: 540px; height: 220px;">Button 250</div>
        <div class="space" style="top: 14040px; left: 120px; width: 420px; height: 1060px;">Button 251</div>
        <div class="space" style="top: 14040px; left: 600px; width: 420px; height: 1060px;">Button 252</div>
        <div class="space" style="top: 14040px; left: 1060px; width: 420px; height: 1060px;">Button 253</div>
        <div class="space" style="top: 14040px; left: 1540px; width: 420px; height: 1060px;">Button 254</div>
        <div class="space" style="top: 14040px; left: 2020px; width: 420px; height: 1060px;">Button 255</div>
        <div class="space" style="top: 14040px; left: 2480px; width: 420px; height: 1060px;">Button 256</div>
        <div class="space" style="top: 14040px; left: 2960px; width: 420px; height: 1060px;">Button 257</div>
        <div class="space" style="top: 14040px; left: 3440px; width: 420px; height: 1060px;">Button 258</div>
        <div class="space" style="top: 14040px; left: 3900px; width: 420px; height: 1060px;">Button 259</div>
        <div class="space" style="top: 14040px; left: 4380px; width: 400px; height: 1060px;">Button 260</div>
        <div class="space" style="top: 14040px; left: 4860px; width: 400px; height: 1060px;">Button 261</div>
        <div class="space" style="top: 14040px; left: 5320px; width: 420px; height: 1060px;">Button 262</div>
        <div class="space" style="top: 14040px; left: 5800px; width: 400px; height: 1060px;">Button 263</div>
        <div class="space" style="top: 14040px; left: 6260px; width: 420px; height: 1060px;">Button 264</div>
        <div class="space" style="top: 14040px; left: 6740px; width: 400px; height: 1060px;">Button 265</div>
        <div class="space" style="top: 14040px; left: 7220px; width: 400px; height: 1060px;">Button 266</div>
        <div class="space" style="top: 14040px; left: 7680px; width: 420px; height: 1060px;">Button 267</div>
        <div class="gate" style="top: 14040px; left: 8200px; width: 1500px; height: 1060px;">메인 게이트</div>
    </div>
    <div class="container" id="page2" style="display: none;">
        <div class="space" style="top: 360.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 268</div>
        <div class="space" style="top: 360.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 269</div>
        <div class="space" style="top: 360.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 270</div>
        <div class="space" style="top: 360.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 271</div>
        <div class="space" style="top: 360.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 272</div>
        <div class="space" style="top: 360.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 273</div>
        <div class="space" style="top: 360.0px; left: 3550.0px; width: 510.0px; height: 1050.0px;">Button 274</div>
        <div class="space" style="top: 360.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 275</div>
        <div class="space" style="top: 360.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 276</div>
        <div class="space" style="top: 360.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 277</div>
        <div class="space" style="top: 360.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 278</div>
        <div class="space" style="top: 360.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 279</div>
        <div class="space" style="top: 360.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 280</div>
        <div class="space" style="top: 360.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 281</div>
        <div class="space" style="top: 360.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 282</div>
        <div class="space" style="top: 360.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 283</div>
        <div class="space" style="top: 360.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 284</div>
        <div class="space" style="top: 1500.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 285</div>
        <div class="space" style="top: 1500.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 286</div>
        <div class="space" style="top: 1500.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 287</div>
        <div class="space" style="top: 1500.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 288</div>
        <div class="space" style="top: 1500.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 289</div>
        <div class="space" style="top: 1500.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 290</div>
        <div class="space" style="top: 1500.0px; left: 3550.0px; width: 510.0px; height: 1050.0px;">Button 291</div>
        <div class="space" style="top: 1500.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 292</div>
        <div class="space" style="top: 1500.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 293</div>
        <div class="space" style="top: 1500.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 294</div>
        <div class="space" style="top: 1500.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 295</div>
        <div class="space" style="top: 1500.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 296</div>
        <div class="space" style="top: 1500.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 297</div>
        <div class="space" style="top: 1500.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 298</div>
        <div class="space" style="top: 1500.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 299</div>
        <div class="space" style="top: 1500.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 300</div>
        <div class="space" style="top: 1500.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 301</div>
        <div class="space" style="top: 3200.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 302</div>
        <div class="space" style="top: 3200.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 303</div>
        <div class="space" style="top: 3200.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 304</div>
        <div class="space" style="top: 3200.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 305</div>
        <div class="space" style="top: 3200.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 306</div>
        <div class="space" style="top: 3200.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 307</div>
        <div class="space" style="top: 3200.0px; left: 3550.0px; width: 480.0px; height: 1050.0px;">Button 308</div>
        <div class="space" style="top: 3200.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 309</div>
        <div class="space" style="top: 3200.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 310</div>
        <div class="space" style="top: 3200.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 311</div>
        <div class="space" style="top: 3200.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 312</div>
        <div class="space" style="top: 3200.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 313</div>
        <div class="space" style="top: 3200.0px; left: 6940.0px; width: 480.0px; height: 1050.0px;">Button 314</div>
        <div class="space" style="top: 3200.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 315</div>
        <div class="space" style="top: 3200.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 316</div>
        <div class="space" style="top: 3200.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 317</div>
        <div class="space" style="top: 3200.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 318</div>
        <div class="space" style="top: 4350.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 319</div>
        <div class="space" style="top: 4350.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 320</div>
        <div class="space" style="top: 4350.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 321</div>
        <div class="space" style="top: 4350.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 322</div>
        <div class="space" style="top: 4350.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 323</div>
        <div class="space" style="top: 4350.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 324</div>
        <div class="space" style="top: 4350.0px; left: 3550.0px; width: 480.0px; height: 1050.0px;">Button 325</div>
        <div class="space" style="top: 4350.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 326</div>
        <div class="space" style="top: 4350.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 327</div>
        <div class="space" style="top: 4350.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 328</div>
        <div class="space" style="top: 4350.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 329</div>
        <div class="space" style="top: 4350.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 330</div>
        <div class="space" style="top: 4350.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 331</div>
        <div class="space" style="top: 4350.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 332</div>
        <div class="space" style="top: 4350.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 333</div>
        <div class="space" style="top: 4350.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 334</div>
        <div class="space" style="top: 4350.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 335</div>
        <div class="space" style="top: 6000.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 336</div>
        <div class="space" style="top: 6000.0px; left: 730.0px; width: 480.0px; height: 1080.0px;">Button 337</div>
        <div class="space" style="top: 6000.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 338</div>
        <div class="space" style="top: 6000.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 339</div>
        <div class="space" style="top: 6000.0px; left: 2440.0px; width: 480.0px; height: 1080.0px;">Button 340</div>
        <div class="space" style="top: 6000.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 341</div>
        <div class="space" style="top: 6000.0px; left: 3550.0px; width: 510.0px; height: 1050.0px;">Button 342</div>
        <div class="space" style="top: 6000.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 343</div>
        <div class="space" style="top: 6000.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 344</div>
        <div class="space" style="top: 6000.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 345</div>
        <div class="space" style="top: 6000.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 346</div>
        <div class="space" style="top: 6000.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 347</div>
        <div class="space" style="top: 6000.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 348</div>
        <div class="space" style="top: 6000.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 349</div>
        <div class="space" style="top: 6000.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 350</div>
        <div class="space" style="top: 6000.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 351</div>
        <div class="space" style="top: 6000.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 352</div>
        <div class="space" style="top: 7200.0px; left: 160.0px; width: 480.0px; height: 1080.0px;">Button 353</div>
        <div class="space" style="top: 7200.0px; left: 730.0px; width: 480.0px; height: 1080.0px;">Button 354</div>
        <div class="space" style="top: 7200.0px; left: 1300.0px; width: 480.0px; height: 1080.0px;">Button 355</div>
        <div class="space" style="top: 7200.0px; left: 1870.0px; width: 480.0px; height: 1080.0px;">Button 356</div>
        <div class="space" style="top: 7200.0px; left: 2440.0px; width: 480.0px; height: 1080.0px;">Button 357</div>
        <div class="space" style="top: 7200.0px; left: 3010.0px; width: 450.0px; height: 1080.0px;">Button 358</div>
        <div class="space" style="top: 7200.0px; left: 3550.0px; width: 510.0px; height: 1080.0px;">Button 359</div>
        <div class="space" style="top: 7200.0px; left: 4120.0px; width: 480.0px; height: 1080.0px;">Button 360</div>
        <div class="space" style="top: 7200.0px; left: 4690.0px; width: 480.0px; height: 1080.0px;">Button 361</div>
        <div class="space" style="top: 7200.0px; left: 5260.0px; width: 480.0px; height: 1080.0px;">Button 362</div>
        <div class="space" style="top: 7200.0px; left: 5830.0px; width: 480.0px; height: 1080.0px;">Button 363</div>
        <div class="space" style="top: 7200.0px; left: 6400.0px; width: 480.0px; height: 1080.0px;">Button 364</div>
        <div class="space" style="top: 7200.0px; left: 6940.0px; width: 510.0px; height: 1080.0px;">Button 365</div>
        <div class="space" style="top: 7200.0px; left: 7510.0px; width: 480.0px; height: 1080.0px;">Button 366</div>
        <div class="space" style="top: 7200.0px; left: 8080.0px; width: 480.0px; height: 1080.0px;">Button 367</div>
        <div class="space" style="top: 7200.0px; left: 8650.0px; width: 480.0px; height: 1080.0px;">Button 368</div>
        <div class="space" style="top: 7200.0px; left: 9220.0px; width: 480.0px; height: 1080.0px;">Button 369</div>
        <div class="space" style="top: 8700.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 370</div>
        <div class="space" style="top: 8700.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 371</div>
        <div class="space" style="top: 8700.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 372</div>
        <div class="space" style="top: 8700.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 373</div>
        <div class="space" style="top: 8700.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 374</div>
        <div class="space" style="top: 8700.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 375</div>
        <div class="space" style="top: 8700.0px; left: 3550.0px; width: 510.0px; height: 1050.0px;">Button 376</div>
        <div class="space" style="top: 8700.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 377</div>
        <div class="space" style="top: 8700.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 378</div>
        <div class="space" style="top: 8700.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 379</div>
        <div class="space" style="top: 8700.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 380</div>
        <div class="space" style="top: 8700.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 381</div>
        <div class="space" style="top: 8700.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 382</div>
        <div class="space" style="top: 8700.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 383</div>
        <div class="space" style="top: 8700.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 384</div>
        <div class="space" style="top: 8700.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 385</div>
        <div class="space" style="top: 8700.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 386</div>
        <div class="space" style="top: 9900.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 387</div>
        <div class="space" style="top: 9900.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 388</div>
        <div class="space" style="top: 9900.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 389</div>
        <div class="space" style="top: 9900.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 390</div>
        <div class="space" style="top: 9900.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 391</div>
        <div class="space" style="top: 9900.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 392</div>
        <div class="space" style="top: 9900.0px; left: 3550.0px; width: 480.0px; height: 1050.0px;">Button 393</div>
        <div class="space" style="top: 9900.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 394</div>
        <div class="space" style="top: 9900.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 395</div>
        <div class="space" style="top: 9900.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 396</div>
        <div class="space" style="top: 9900.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 397</div>
        <div class="space" style="top: 9900.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 398</div>
        <div class="space" style="top: 9900.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 399</div>
        <div class="space" style="top: 9900.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 400</div>
        <div class="space" style="top: 9900.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 401</div>
        <div class="space" style="top: 9900.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 402</div>
        <div class="space" style="top: 9900.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 403</div>
        <div class="space" style="top: 11300.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 404</div>
        <div class="space" style="top: 11300.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 405</div>
        <div class="space" style="top: 11300.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 406</div>
        <div class="space" style="top: 11300.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 407</div>
        <div class="space" style="top: 11300.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 408</div>
        <div class="space" style="top: 11300.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 409</div>
        <div class="space" style="top: 11300.0px; left: 3550.0px; width: 510.0px; height: 1050.0px;">Button 410</div>
        <div class="space" style="top: 11300.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 411</div>
        <div class="space" style="top: 11300.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 412</div>
        <div class="space" style="top: 11300.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 413</div>
        <div class="space" style="top: 11300.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 414</div>
        <div class="space" style="top: 11300.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 415</div>
        <div class="space" style="top: 11300.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 416</div>
        <div class="space" style="top: 11300.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 417</div>
        <div class="space" style="top: 11300.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 418</div>
        <div class="space" style="top: 11300.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 419</div>
        <div class="space" style="top: 11300.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 420</div>
        <div class="space" style="top: 12500.0px; left: 160.0px; width: 480.0px; height: 1080.0px;">Button 421</div>
        <div class="space" style="top: 12500.0px; left: 730.0px; width: 480.0px; height: 1080.0px;">Button 422</div>
        <div class="space" style="top: 12500.0px; left: 1300.0px; width: 480.0px; height: 1080.0px;">Button 423</div>
        <div class="space" style="top: 12500.0px; left: 1870.0px; width: 480.0px; height: 1080.0px;">Button 424</div>
        <div class="space" style="top: 12500.0px; left: 2440.0px; width: 480.0px; height: 1080.0px;">Button 425</div>
        <div class="space" style="top: 12500.0px; left: 3010.0px; width: 450.0px; height: 1080.0px;">Button 426</div>
        <div class="space" style="top: 12500.0px; left: 3550.0px; width: 510.0px; height: 1080.0px;">Button 427</div>
        <div class="space" style="top: 12500.0px; left: 4120.0px; width: 480.0px; height: 1080.0px;">Button 428</div>
        <div class="space" style="top: 12500.0px; left: 4690.0px; width: 480.0px; height: 1080.0px;">Button 429</div>
        <div class="space" style="top: 12500.0px; left: 5260.0px; width: 480.0px; height: 1080.0px;">Button 430</div>
        <div class="space" style="top: 12500.0px; left: 5830.0px; width: 480.0px; height: 1080.0px;">Button 431</div>
        <div class="space" style="top: 12500.0px; left: 6400.0px; width: 480.0px; height: 1080.0px;">Button 432</div>
        <div class="space" style="top: 12500.0px; left: 6940.0px; width: 510.0px; height: 1080.0px;">Button 433</div>
        <div class="space" style="top: 12500.0px; left: 7510.0px; width: 480.0px; height: 1080.0px;">Button 434</div>
        <div class="space" style="top: 12500.0px; left: 8080.0px; width: 480.0px; height: 1080.0px;">Button 435</div>
        <div class="space" style="top: 12500.0px; left: 8650.0px; width: 480.0px; height: 1080.0px;">Button 436</div>
        <div class="space" style="top: 12500.0px; left: 9220.0px; width: 480.0px; height: 1080.0px;">Button 437</div>
        <div class="space" style="top: 14100.0px; left: 160.0px; width: 480.0px; height: 1080.0px;">Button 438</div>
        <div class="space" style="top: 14100.0px; left: 730.0px; width: 480.0px; height: 1080.0px;">Button 439</div>
        <div class="space" style="top: 14100.0px; left: 1300.0px; width: 480.0px; height: 1080.0px;">Button 440</div>
        <div class="space" style="top: 14100.0px; left: 1870.0px; width: 480.0px; height: 1080.0px;">Button 441</div>
        <div class="space" style="top: 14100.0px; left: 2440.0px; width: 480.0px; height: 1080.0px;">Button 442</div>
        <div class="space" style="top: 14100.0px; left: 3010.0px; width: 450.0px; height: 1080.0px;">Button 443</div>
        <div class="space" style="top: 14100.0px; left: 3550.0px; width: 510.0px; height: 1080.0px;">Button 444</div>
        <div class="space" style="top: 14100.0px; left: 4120.0px; width: 480.0px; height: 1080.0px;">Button 445</div>
        <div class="space" style="top: 14100.0px; left: 4690.0px; width: 480.0px; height: 1080.0px;">Button 446</div>
        <div class="space" style="top: 14100.0px; left: 5260.0px; width: 480.0px; height: 1080.0px;">Button 447</div>
        <div class="space" style="top: 14100.0px; left: 5830.0px; width: 480.0px; height: 1080.0px;">Button 448</div>
        <div class="space" style="top: 14100.0px; left: 6400.0px; width: 480.0px; height: 1080.0px;">Button 449</div>
        <div class="space" style="top: 14100.0px; left: 6940.0px; width: 510.0px; height: 1080.0px;">Button 450</div>
        <div class="space" style="top: 14100.0px; left: 7510.0px; width: 480.0px; height: 1080.0px;">Button 451</div>
        <div class="space" style="top: 14100.0px; left: 8080.0px; width: 480.0px; height: 1080.0px;">Button 452</div>
        <div class="space" style="top: 14100.0px; left: 8650.0px; width: 480.0px; height: 1080.0px;">Button 453</div>
        <div class="space" style="top: 14100.0px; left: 9220.0px; width: 480.0px; height: 1080.0px;">Button 454</div>
        <div class="space" style="top: 15300.0px; left: 160.0px; width: 480.0px; height: 1050.0px;">Button 455</div>
        <div class="space" style="top: 15300.0px; left: 730.0px; width: 480.0px; height: 1050.0px;">Button 456</div>
        <div class="space" style="top: 15300.0px; left: 1300.0px; width: 480.0px; height: 1050.0px;">Button 457</div>
        <div class="space" style="top: 15300.0px; left: 1870.0px; width: 480.0px; height: 1050.0px;">Button 458</div>
        <div class="space" style="top: 15300.0px; left: 2440.0px; width: 480.0px; height: 1050.0px;">Button 459</div>
        <div class="space" style="top: 15300.0px; left: 3010.0px; width: 450.0px; height: 1050.0px;">Button 460</div>
        <div class="space" style="top: 15300.0px; left: 3550.0px; width: 510.0px; height: 1050.0px;">Button 461</div>
        <div class="space" style="top: 15300.0px; left: 4120.0px; width: 480.0px; height: 1050.0px;">Button 462</div>
        <div class="space" style="top: 15300.0px; left: 4690.0px; width: 480.0px; height: 1050.0px;">Button 463</div>
        <div class="space" style="top: 15300.0px; left: 5260.0px; width: 480.0px; height: 1050.0px;">Button 464</div>
        <div class="space" style="top: 15300.0px; left: 5830.0px; width: 480.0px; height: 1050.0px;">Button 465</div>
        <div class="space" style="top: 15300.0px; left: 6400.0px; width: 480.0px; height: 1050.0px;">Button 466</div>
        <div class="space" style="top: 15300.0px; left: 6940.0px; width: 510.0px; height: 1050.0px;">Button 467</div>
        <div class="space" style="top: 15300.0px; left: 7510.0px; width: 480.0px; height: 1050.0px;">Button 468</div>
        <div class="space" style="top: 15300.0px; left: 8080.0px; width: 480.0px; height: 1050.0px;">Button 469</div>
        <div class="space" style="top: 15300.0px; left: 8650.0px; width: 480.0px; height: 1050.0px;">Button 470</div>
        <div class="space" style="top: 15300.0px; left: 9220.0px; width: 480.0px; height: 1050.0px;">Button 471</div>
        <div class="gate" style="top: 16900.0px; left: 100.0px; width: 1200.0px; height: 1350.0px;">메인 게이트</div>
        <div class="space" style="top: 16900.0px; left: 1360.0px; width: 570.0px; height: 1350.0px;">Button 472</div>
        <div class="space" style="top: 16900.0px; left: 1990.0px; width: 570.0px; height: 1350.0px;">Button 473</div>
        <div class="space" style="top: 16900.0px; left: 2650.0px; width: 570.0px; height: 1350.0px;">Button 474</div>
        <div class="space" style="top: 16900.0px; left: 3310.0px; width: 570.0px; height: 1350.0px;">Button 475</div>
        <div class="space" style="top: 16900.0px; left: 3940.0px; width: 570.0px; height: 1350.0px;">Button 476</div>
        <div class="space" style="top: 16900.0px; left: 4600.0px; width: 570.0px; height: 1350.0px;">Button 477</div>
        <div class="space" style="top: 16900.0px; left: 5230.0px; width: 570.0px; height: 1350.0px;">Button 478</div>
        <div class="space" style="top: 16900.0px; left: 5890.0px; width: 570.0px; height: 1350.0px;">Button 479</div>
        <div class="space" style="top: 16900.0px; left: 6550.0px; width: 570.0px; height: 1350.0px;">Button 480</div>
        <div class="space" style="top: 16900.0px; left: 7180.0px; width: 570.0px; height: 1350.0px;">Button 481</div>
        <div class="space" style="top: 16900.0px; left: 7840.0px; width: 570.0px; height: 1350.0px;">Button 482</div>
        <div class="space" style="top: 16900.0px; left: 8470.0px; width: 570.0px; height: 1350.0px;">Button 483</div>
        <div class="space" style="top: 16900.0px; left: 9130.0px; width: 570.0px; height: 1350.0px;">Button 484</div>
    </div>
    <div class="container" id="page3" style="display: none;">
        <div class="space" style="top: 176px; left: 8294px; width: 1078px; height: 396px;">Button 485</div>
        <div class="space" style="top: 638px; left: 264px; width: 484px; height: 1034px;">Button 486</div>
        <div class="space" style="top: 638px; left: 814px; width: 506px; height: 1034px;">Button 487</div>
        <div class="space" style="top: 638px; left: 1386px; width: 506px; height: 1034px;">Button 488</div>
        <div class="space" style="top: 638px; left: 1936px; width: 506px; height: 1034px;">Button 489</div>
        <div class="space" style="top: 638px; left: 2508px; width: 506px; height: 1034px;">Button 490</div>
        <div class="space" style="top: 638px; left: 3080px; width: 506px; height: 1034px;">Button 491</div>
        <div class="space" style="top: 638px; left: 3630px; width: 506px; height: 1034px;">Button 492</div>
        <div class="space" style="top: 638px; left: 4202px; width: 506px; height: 1034px;">Button 493</div>
        <div class="space" style="top: 638px; left: 4774px; width: 484px; height: 1034px;">Button 494</div>
        <div class="space" style="top: 638px; left: 5324px; width: 506px; height: 1034px;">Button 495</div>
        <div class="space" style="top: 638px; left: 5896px; width: 1078px; height: 374px;">Button 496</div>
        <div class="space" style="top: 638px; left: 8294px; width: 1078px; height: 418px;">Button 497</div>
        <div class="space" style="top: 1078px; left: 5896px; width: 1078px; height: 374px;">Button 498</div>
        <div class="space" style="top: 1122px; left: 8294px; width: 1078px; height: 396px;">Button 499</div>
        <div class="space" style="top: 1518px; left: 5896px; width: 1078px; height: 374px;">Button 500</div>
        <div class="space" style="top: 1584px; left: 8294px; width: 1078px; height: 396px;">Button 501</div>
        <div class="space" style="top: 1738px; left: 264px; width: 484px; height: 1034px;">Button 502</div>
        <div class="space" style="top: 1738px; left: 814px; width: 506px; height: 1034px;">Button 503</div>
        <div class="space" style="top: 1738px; left: 1386px; width: 506px; height: 1034px;">Button 504</div>
        <div class="space" style="top: 1738px; left: 1936px; width: 506px; height: 1034px;">Button 505</div>
        <div class="space" style="top: 1738px; left: 2508px; width: 506px; height: 1034px;">Button 506</div>
        <div class="space" style="top: 1738px; left: 3080px; width: 506px; height: 1034px;">Button 507</div>
        <div class="space" style="top: 1738px; left: 3630px; width: 506px; height: 1034px;">Button 508</div>
        <div class="space" style="top: 1738px; left: 4202px; width: 506px; height: 1034px;">Button 509</div>
        <div class="space" style="top: 1738px; left: 4774px; width: 484px; height: 1034px;">Button 510</div>
        <div class="space" style="top: 1738px; left: 5324px; width: 506px; height: 1034px;">Button 511</div>
        <div class="space" style="top: 1958px; left: 5896px; width: 1078px; height: 374px;">Button 512</div>
        <div class="space" style="top: 2046px; left: 8294px; width: 1078px; height: 418px;">Button 513</div>
        <div class="space" style="top: 2398px; left: 5896px; width: 1078px; height: 374px;">Button 514</div>
        <div class="space" style="top: 2530px; left: 8294px; width: 1078px; height: 396px;">Button 515</div>
        <div class="space" style="top: 2992px; left: 8294px; width: 1078px; height: 396px;">Button 516</div>
        <div class="space" style="top: 3454px; left: 8294px; width: 1078px; height: 418px;">Button 517</div>
        <div class="space" style="top: 3542px; left: 264px; width: 484px; height: 1034px;">Button 518</div>
        <div class="space" style="top: 3542px; left: 814px; width: 506px; height: 1034px;">Button 519</div>
        <div class="space" style="top: 3542px; left: 1386px; width: 506px; height: 1034px;">Button 520</div>
        <div class="space" style="top: 3542px; left: 1936px; width: 506px; height: 1034px;">Button 521</div>
        <div class="space" style="top: 3542px; left: 2508px; width: 506px; height: 1034px;">Button 522</div>
        <div class="space" style="top: 3542px; left: 3080px; width: 506px; height: 1034px;">Button 523</div>
        <div class="space" style="top: 3542px; left: 3630px; width: 506px; height: 1034px;">Button 524</div>
        <div class="space" style="top: 3542px; left: 4202px; width: 506px; height: 1034px;">Button 525</div>
        <div class="space" style="top: 3542px; left: 4774px; width: 484px; height: 1034px;">Button 526</div>
        <div class="space" style="top: 3542px; left: 5324px; width: 506px; height: 1034px;">Button 527</div>
        <div class="space" style="top: 3542px; left: 5896px; width: 1078px; height: 374px;">Button 528</div>
        <div class="space" style="top: 3938px; left: 8294px; width: 1078px; height: 396px;">Button 529</div>
        <div class="space" style="top: 3982px; left: 5896px; width: 1078px; height: 374px;">Button 530</div>
        <div class="space" style="top: 4400px; left: 8294px; width: 1078px; height: 396px;">Button 531</div>
        <div class="space" style="top: 4422px; left: 5896px; width: 1078px; height: 374px;">Button 532</div>
        <div class="space" style="top: 4642px; left: 264px; width: 484px; height: 1034px;">Button 533</div>
        <div class="space" style="top: 4642px; left: 814px; width: 506px; height: 1034px;">Button 534</div>
        <div class="space" style="top: 4642px; left: 1386px; width: 506px; height: 1034px;">Button 535</div>
        <div class="space" style="top: 4642px; left: 1936px; width: 506px; height: 1034px;">Button 536</div>
        <div class="space" style="top: 4642px; left: 2508px; width: 506px; height: 1034px;">Button 537</div>
        <div class="space" style="top: 4642px; left: 3080px; width: 506px; height: 1034px;">Button 538</div>
        <div class="space" style="top: 4642px; left: 3630px; width: 506px; height: 1034px;">Button 539</div>
        <div class="space" style="top: 4642px; left: 4202px; width: 506px; height: 1034px;">Button 540</div>
        <div class="space" style="top: 4642px; left: 4774px; width: 484px; height: 1034px;">Button 541</div>
        <div class="space" style="top: 4642px; left: 5324px; width: 506px; height: 1034px;">Button 542</div>
        <div class="space" style="top: 4862px; left: 5896px; width: 1078px; height: 374px;">Button 543</div>
        <div class="space" style="top: 4862px; left: 8294px; width: 1078px; height: 418px;">Button 544</div>
        <div class="space" style="top: 5302px; left: 5896px; width: 1078px; height: 374px;">Button 545</div>
        <div class="space" style="top: 5346px; left: 8294px; width: 1078px; height: 396px;">Button 546</div>
        <div class="space" style="top: 5808px; left: 8294px; width: 1078px; height: 396px;">Button 547</div>
        <div class="space" style="top: 6270px; left: 8294px; width: 1078px; height: 418px;">Button 548</div>
        <div class="space" style="top: 6446px; left: 264px; width: 506px; height: 1034px;">Button 549</div>
        <div class="space" style="top: 6446px; left: 814px; width: 506px; height: 1034px;">Button 550</div>
        <div class="space" style="top: 6446px; left: 1386px; width: 506px; height: 1034px;">Button 551</div>
        <div class="space" style="top: 6446px; left: 1936px; width: 506px; height: 1034px;">Button 552</div>
        <div class="space" style="top: 6446px; left: 2508px; width: 506px; height: 1034px;">Button 553</div>
        <div class="space" style="top: 6446px; left: 3080px; width: 506px; height: 1034px;">Button 554</div>
        <div class="space" style="top: 6446px; left: 3630px; width: 506px; height: 1034px;">Button 555</div>
        <div class="space" style="top: 6446px; left: 4202px; width: 506px; height: 1034px;">Button 556</div>
        <div class="space" style="top: 6446px; left: 4774px; width: 484px; height: 1034px;">Button 557</div>
        <div class="space" style="top: 6446px; left: 5324px; width: 506px; height: 1034px;">Button 558</div>
        <div class="space" style="top: 6446px; left: 5896px; width: 1078px; height: 374px;">Button 559</div>
        <div class="space" style="top: 6754px; left: 8294px; width: 1078px; height: 396px;">Button 560</div>
        <div class="space" style="top: 6886px; left: 5896px; width: 1078px; height: 374px;">Button 561</div>
        <div class="space" style="top: 7216px; left: 8294px; width: 1078px; height: 396px;">Button 562</div>
        <div class="space" style="top: 7326px; left: 5896px; width: 1078px; height: 374px;">Button 563</div>
        <div class="space" style="top: 7546px; left: 264px; width: 484px; height: 1034px;">Button 564</div>
        <div class="space" style="top: 7546px; left: 814px; width: 506px; height: 1034px;">Button 565</div>
        <div class="space" style="top: 7546px; left: 1386px; width: 506px; height: 1034px;">Button 566</div>
        <div class="space" style="top: 7546px; left: 1936px; width: 506px; height: 1034px;">Button 567</div>
        <div class="space" style="top: 7546px; left: 2508px; width: 506px; height: 1034px;">Button 568</div>
        <div class="space" style="top: 7546px; left: 3080px; width: 506px; height: 1034px;">Button 569</div>
        <div class="space" style="top: 7546px; left: 3630px; width: 506px; height: 1034px;">Button 570</div>
        <div class="space" style="top: 7546px; left: 4202px; width: 506px; height: 1034px;">Button 571</div>
        <div class="space" style="top: 7546px; left: 4774px; width: 484px; height: 1034px;">Button 572</div>
        <div class="space" style="top: 7546px; left: 5324px; width: 506px; height: 1034px;">Button 573</div>
        <div class="space" style="top: 7678px; left: 8294px; width: 1078px; height: 418px;">Button 574</div>
        <div class="space" style="top: 7766px; left: 5896px; width: 1078px; height: 374px;">Button 575</div>
        <div class="space" style="top: 8162px; left: 8294px; width: 1078px; height: 396px;">Button 576</div>
        <div class="space" style="top: 8206px; left: 5896px; width: 1078px; height: 374px;">Button 577</div>
        <div class="space" style="top: 8624px; left: 8294px; width: 1078px; height: 396px;">Button 578</div>
        <div class="space" style="top: 9086px; left: 8294px; width: 1078px; height: 418px;">Button 579</div>
        <div class="space" style="top: 9680px; left: 264px; width: 484px; height: 1034px;">Button 580</div>
        <div class="space" style="top: 9680px; left: 814px; width: 506px; height: 1034px;">Button 581</div>
        <div class="space" style="top: 9680px; left: 1386px; width: 506px; height: 1034px;">Button 582</div>
        <div class="space" style="top: 9680px; left: 1936px; width: 506px; height: 1034px;">Button 583</div>
        <div class="space" style="top: 9680px; left: 2508px; width: 506px; height: 1034px;">Button 584</div>
        <div class="space" style="top: 9680px; left: 3080px; width: 506px; height: 1034px;">Button 585</div>
        <div class="space" style="top: 9680px; left: 3630px; width: 506px; height: 1034px;">Button 586</div>
        <div class="space" style="top: 9680px; left: 4202px; width: 506px; height: 1034px;">Button 587</div>
        <div class="space" style="top: 9680px; left: 4774px; width: 484px; height: 1034px;">Button 588</div>
        <div class="space" style="top: 9680px; left: 5324px; width: 1078px; height: 374px;">Button 589</div>
        <div class="space" style="top: 10120px; left: 5324px; width: 1078px; height: 374px;">Button 590</div>
        <div class="space" style="top: 10252px; left: 8294px; width: 1100px; height: 418px;">Button 591</div>
        <div class="space" style="top: 10560px; left: 5324px; width: 1078px; height: 374px;">Button 592</div>
        <div class="space" style="top: 10714px; left: 8294px; width: 1100px; height: 418px;">Button 593</div>
        <div class="space" style="top: 10780px; left: 264px; width: 484px; height: 1034px;">Button 594</div>
        <div class="space" style="top: 10780px; left: 814px; width: 506px; height: 1034px;">Button 595</div>
        <div class="space" style="top: 10780px; left: 1386px; width: 506px; height: 1034px;">Button 596</div>
        <div class="space" style="top: 10780px; left: 1936px; width: 506px; height: 1034px;">Button 597</div>
        <div class="space" style="top: 10780px; left: 2508px; width: 506px; height: 1034px;">Button 598</div>
        <div class="space" style="top: 10780px; left: 3080px; width: 506px; height: 1034px;">Button 599</div>
        <div class="space" style="top: 10780px; left: 3630px; width: 506px; height: 1034px;">Button 600</div>
        <div class="space" style="top: 10780px; left: 4202px; width: 506px; height: 1034px;">Button 601</div>
        <div class="space" style="top: 10780px; left: 4774px; width: 484px; height: 1034px;">Button 602</div>
        <div class="space" style="top: 11000px; left: 5324px; width: 1078px; height: 374px;">Button 603</div>
        <div class="space" style="top: 11198px; left: 8294px; width: 1100px; height: 396px;">Button 604</div>
        <div class="space" style="top: 11440px; left: 5324px; width: 1078px; height: 374px;">Button 605</div>
        <div class="space" style="top: 11660px; left: 8294px; width: 1100px; height: 418px;">Button 606</div>
        <div class="space" style="top: 12122px; left: 8294px; width: 1100px; height: 418px;">Button 607</div>
        <div class="space" style="top: 12606px; left: 8294px; width: 1100px; height: 396px;">Button 608</div>
        <div class="space" style="top: 12716px; left: 264px; width: 484px; height: 1034px;">Button 609</div>
        <div class="space" style="top: 12716px; left: 814px; width: 506px; height: 1034px;">Button 610</div>
        <div class="space" style="top: 12716px; left: 1386px; width: 506px; height: 1034px;">Button 611</div>
        <div class="space" style="top: 12716px; left: 1936px; width: 506px; height: 1034px;">Button 612</div>
        <div class="space" style="top: 12716px; left: 2508px; width: 506px; height: 1034px;">Button 613</div>
        <div class="space" style="top: 12716px; left: 3080px; width: 506px; height: 1034px;">Button 614</div>
        <div class="space" style="top: 12716px; left: 3630px; width: 506px; height: 1034px;">Button 615</div>
        <div class="space" style="top: 12716px; left: 4202px; width: 1078px; height: 374px;">Button 616</div>
        <div class="space" style="top: 13068px; left: 8294px; width: 1100px; height: 418px;">Button 617</div>
        <div class="space" style="top: 13156px; left: 4202px; width: 1078px; height: 374px;">Button 618</div>
        <div class="space" style="top: 13530px; left: 8294px; width: 1100px; height: 418px;">Button 619</div>
        <div class="space" style="top: 13596px; left: 4202px; width: 1078px; height: 374px;">Button 620</div>
        <div class="space" style="top: 13794px; left: 264px; width: 506px; height: 1034px;">Button 621</div>
        <div class="space" style="top: 13794px; left: 814px; width: 506px; height: 1034px;">Button 622</div>
        <div class="space" style="top: 13794px; left: 1386px; width: 506px; height: 1034px;">Button 623</div>
        <div class="space" style="top: 13794px; left: 1936px; width: 506px; height: 1034px;">Button 624</div>
        <div class="space" style="top: 13794px; left: 2508px; width: 506px; height: 1034px;">Button 625</div>
        <div class="space" style="top: 13794px; left: 3080px; width: 506px; height: 1034px;">Button 626</div>
        <div class="space" style="top: 13794px; left: 3630px; width: 506px; height: 1034px;">Button 627</div>
        <div class="space" style="top: 14014px; left: 8294px; width: 1100px; height: 396px;">Button 628</div>
        <div class="space" style="top: 14476px; left: 8294px; width: 1100px; height: 418px;">Button 629</div>
        <div class="space" style="top: 14938px; left: 8294px; width: 1100px; height: 418px;">Button 630</div>
        <div class="space" style="top: 15422px; left: 8294px; width: 1100px; height: 396px;">Button 631</div>
        <div class="space" style="top: 15532px; left: 264px; width: 1166px; height: 440px;">Button 632</div>
        <div class="space" style="top: 15884px; left: 3080px; width: 418px; height: 1122px;">Button 633</div>
        <div class="space" style="top: 15884px; left: 3564px; width: 396px; height: 1122px;">Button 634</div>
        <div class="space" style="top: 15884px; left: 4026px; width: 418px; height: 1122px;">Button 635</div>
        <div class="space" style="top: 15884px; left: 4510px; width: 396px; height: 1122px;">Button 636</div>
        <div class="space" style="top: 15884px; left: 4972px; width: 418px; height: 1122px;">Button 637</div>
        <div class="space" style="top: 15884px; left: 5456px; width: 418px; height: 1122px;">Button 638</div>
        <div class="space" style="top: 15884px; left: 5918px; width: 418px; height: 1122px;">Button 639</div>
        <div class="space" style="top: 15884px; left: 6402px; width: 418px; height: 1122px;">Button 640</div>
        <div class="space" style="top: 15884px; left: 6864px; width: 418px; height: 1122px;">Button 641</div>
        <div class="space" style="top: 15884px; left: 7348px; width: 418px; height: 1122px;">Button 642</div>
        <div class="space" style="top: 15884px; left: 7810px; width: 418px; height: 1122px;">Button 643</div>
        <div class="space" style="top: 15884px; left: 8294px; width: 1100px; height: 1122px;">Button 644</div>
        <div class="space" style="top: 16038px; left: 264px; width: 1166px; height: 462px;">Button 645</div>
        <div class="space" style="top: 16566px; left: 264px; width: 1166px; height: 440px;">Button 646</div>
    </div>
    <script>
        // 예: 장애인 주차 구역 버튼 번호 (1-based)
        const DISABLED_PARKING_BUTTONS = [
          2, 3, 4, 262, 263, 264, 265, 266, 267,
          472, 473, 474, 475, 476, 477,
          576, 578, 579,
          591, 593,
          604, 606, 607, 608
        ];

        function showPage(pageNumber) {
            const pages = document.querySelectorAll('.container');
            pages.forEach(page => page.style.display = 'none');
            const selectedPage = document.getElementById('page' + pageNumber);
            if (selectedPage) {
                selectedPage.style.display = 'block';
            }
        }

        function fetchAndUpdateButtons() {
      fetch('/get-button-status')
        .then(res => res.json())
        .then(data => {
          const buttons = document.querySelectorAll('.space');
          let page1Parked = 0; // 1~267
          let page2Parked = 0; // 268~484
          let page3Parked = 0; // 485~646
          buttons.forEach((btn, idx) => {
            const buttonNumber = idx + 1;
            const status = data[idx];

            if (status === 0) {
              // 빈자리
              if (DISABLED_PARKING_BUTTONS.includes(buttonNumber)) {
                btn.style.backgroundColor = 'orange'; 
              } else {
                btn.style.backgroundColor = 'greenyellow';
              }
            } else {
              // 차 있음
              btn.style.backgroundColor = 'red';
            }
              if (status === 1) {
            if (buttonNumber <= 267) {
              page1Parked++;
            } else if (buttonNumber <= 484) {
              page2Parked++;
            } else {
              page3Parked++;
            }
          }
          });
           const zone1Total = 267; // 좌측 구역
        const zone2Total = 217; // 중간 구역
        const zone3Total = 162; // 우측 구역

        document.getElementById('zone1-info').textContent =
          `좌측 구역: 총 ${zone1Total}칸 중 주차 ${page1Parked}대 (남은 ${zone1Total - page1Parked}칸)`;
        document.getElementById('zone2-info').textContent =
          `중간 구역: 총 ${zone2Total}칸 중 주차 ${page2Parked}대 (남은 ${zone2Total - page2Parked}칸)`;
        document.getElementById('zone3-info').textContent =
          `우측 구역: 총 ${zone3Total}칸 중 주차 ${page3Parked}대 (남은 ${zone3Total - page3Parked}칸)`;
      
        })
      .catch(error => console.error('Error fetching button status:', error));
        }

        setInterval(fetchAndUpdateButtons, 1000);

        document.addEventListener('DOMContentLoaded', () => {
            fetchAndUpdateButtons();
            showPage(1);
        });
    </script>
</body>
</html>
"""

# ---------------------------
# 4) 전역 변수 (버튼 상태)
# ---------------------------
LATEST_DATA = None

def lambda_handler(event, context):
    global LATEST_DATA

    path = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    print(f"[Lambda] {method} {path}")

    # ------------------------
    # 4-1) POST /update-button-status (로컬 PC → 이 Lambda)
    # ------------------------
    if path == "/update-button-status" and method == "POST":
        body_str = event.get("body", "{}")
        try:
            data_list = json.loads(body_str)
        except:
            data_list = []
        
        LATEST_DATA = data_list
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Update success"})
        }
    
    # ------------------------
    # 4-2) GET /get-button-status (웹브라우저가 버튼 상태 요청)
    # ------------------------
    elif path == "/get-button-status" and method == "GET":
        if LATEST_DATA is None:
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps([])
            }
        else:
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(LATEST_DATA)
            }

    # ------------------------
    # 4-3) GET /manifest.json (PWA Manifest)
    # ------------------------
    elif path == "/manifest.json" and method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": MANIFEST_JSON
        }

    # ------------------------
    # 4-4) GET /service-worker.js (Service Worker)
    # ------------------------
    elif path == "/service-worker.js" and method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/javascript; charset=utf-8"
            },
            "body": SERVICE_WORKER_JS
        }

    # ------------------------
    # 4-5) GET / (메인 HTML 페이지)
    # ------------------------
    elif path == "/" and method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8"
            },
            "body": HTML_CONTENT
        }

    # ------------------------
    # 그 외 -> 404
    # ------------------------
    else:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "text/plain"},
            "body": "Not Found"
        }
