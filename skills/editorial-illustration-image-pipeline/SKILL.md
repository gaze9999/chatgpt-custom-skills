---
name: editorial-illustration-image-pipeline
description: 以使用者提供的圖片為視覺依據，結合可選調整與內建 editorial illustration 基礎 prompt，直接生成插畫。
metadata:
  short-description: 圖片輸入加上可選調整的直接插畫生成 pipeline
---

# Editorial Illustration 圖片 Pipeline

這是純圖片生成 pipeline。條件足夠時直接生成圖片，不將最終 prompt、組裝過程或分析當成主要輸出。

## 輸入與處理

- 必須有目前對話中可用的 `SOURCE_IMAGE`；缺圖時只要求使用者提供圖片。
- 使用者可自然語言指定構圖、主體、留白、場景、色彩、氛圍、質感、文字或風格微調；未提供的調整不自行補足。
- 每次生成都讀取並套用 [Base Prompt](references/base-prompt.md)。使用者當次調整可覆蓋其中可調整的視覺細節，但不可移除核心 pipeline 約束。

## 核心約束

- 來源圖提供主體、姿態、物件、關係、氛圍與色彩等視覺依據。
- 每張來源圖獨立輸出一張完整插畫；不合併為 collage、split-screen 或 before/after。
- 不直接顯示或混入原始照片。
- 多圖時逐張套用 Base Prompt 與相應調整；除非使用者明確要求合成，否則不混合不同圖片的元素。

有可用圖片且要求可執行時，直接使用可用 image-generation capability 交付結果。
