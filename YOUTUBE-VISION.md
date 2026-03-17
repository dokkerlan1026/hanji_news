# YouTube Vision 工具鏈

## 目標

讓 agent 分析 YouTube 時，不只依賴聲音、ASR 與字幕，而是能真正做基本的視覺理解。

## 已安裝的本地工具

這些工具都安裝在 workspace 內，不需要系統層 root 權限：

- `./.local/bin/yt-dlp`
  - 下載 YouTube 影片 / 音訊 / metadata
- `./.local/lib/youtube-vision/node_modules/ffmpeg-static/ffmpeg`
  - 擷取影格、抽音訊、裁切片段、場景抽樣
- `./.local/lib/youtube-vision/node_modules/ffprobe-static/bin/linux/x64/ffprobe`
  - 讀影片長度、解析度、streams 資訊
- `tesseract.js` (Node package)
  - OCR 畫面文字
- `jimp` (Node package)
  - 基本圖片前處理

## 建議分析流程

1. 用 `yt-dlp` 下載影片或只抓 metadata
2. 用 `ffprobe` 讀影片資訊
3. 用 `ffmpeg` 每隔 N 秒抽影格，或用 scene change 規則抽關鍵影格
4. 對影格做 OCR，讀取畫面中的文字
5. 把視覺觀察和字幕 / 音訊分開整理
6. 最後再做綜合判斷，避免只靠字幕腦補

## 參考命令

### 1. 看影片 metadata

```bash
./.local/bin/yt-dlp --dump-single-json "YOUTUBE_URL"
```

### 2. 下載影片

```bash
./.local/bin/yt-dlp -f "bv*+ba/b" -o "downloads/%(title)s.%(ext)s" "YOUTUBE_URL"
```

### 3. 讀影片資訊

```bash
./.local/lib/youtube-vision/node_modules/ffprobe-static/bin/linux/x64/ffprobe -v error -show_format -show_streams "video.mp4"
```

### 4. 每 10 秒抽一張圖

```bash
./.local/lib/youtube-vision/node_modules/ffmpeg-static/ffmpeg -i "video.mp4" -vf fps=1/10 "frames/frame_%04d.jpg"
```

### 5. 場景切換抽樣

```bash
./.local/lib/youtube-vision/node_modules/ffmpeg-static/ffmpeg -i "video.mp4" -vf "select='gt(scene,0.35)',showinfo" -vsync vfr "frames/scene_%04d.jpg"
```

## 之後可再補的東西

如果未來要更強：

- OpenCV 做鏡頭變化 / 物件追蹤
- Whisper 或其他 ASR 做語音逐字稿
- 多模態模型做影格級摘要與時間對齊
- 專門的 YouTube 分析腳本，把下載、抽圖、OCR、摘要串起來
