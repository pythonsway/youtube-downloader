pyinstaller \
--clean \
--noconfirm \
--onefile \
--name=YTDownloader \
--hidden-import=pkg_resources.py2_warn \
--hidden-import=pkg_resources.markers \
--icon="assets/favicon.ico" \
--add-data="assets/*;assets" \
--version-file=file_version_info.txt \
__main__.py \
--upx-dir="D:\upx" \
2> build.txt


# --windowed \
# --debug=all \
# --log-level=DEBUG \
# --debug=imports \

# pyinstaller --noconfirm --onefile --windowed --icon "F:/my_projects/youtube-downloader/assets/favicon.ico" --name "YTDownloader" --clean --version-file "F:/my_projects/youtube-downloader/file_version_info.txt" --add-data "F:/my_projects/youtube-downloader/assets;assets/"  "F:/my_projects/youtube-downloader/__main__.py"

# failed to execute script pyiboot01_bootstrap