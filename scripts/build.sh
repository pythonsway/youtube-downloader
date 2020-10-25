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