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
--upx-dir="D:\upx" \
--paths "F:\my_projects\youtube-downloader" \
__main__.py \
2> build.txt

# --windowed \
# --debug=all \
# --log-level=DEBUG \
# --debug=imports \