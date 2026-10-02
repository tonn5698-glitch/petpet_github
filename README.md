# maimai-petpet (pygame)

Click/chạm để vuốt, tap liên tục (<300ms/lần) để combo, combo 50 = nổ. SPACE = tap, ESC = thoát.

## Chạy từ source
    pip install pygame
    python main.py

## Build exe
- GitHub Actions: push lên `main` (hoặc Actions > Build Windows exe > Run workflow) -> tải `petpet-windows` ở mục Artifacts.
- Push tag `v1.0` -> exe tự đính vào GitHub Release.
- Local (Windows): chạy `build_exe.bat` -> `dist\petpet.exe`.
