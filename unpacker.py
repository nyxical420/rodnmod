import errno
from zipfile import ZipFile
from os import execv, path, chdir

chdir(path.dirname(path.abspath(__file__)))

if path.exists("update.zip"):
    with ZipFile("update.zip", 'r') as zip_ref:
        for file in zip_ref.namelist():
            try:
                zip_ref.extract(file)
            except OSError as e:
                if e.errno == errno.EACCES:
                    print(f"Skipped '{file}' as it is currently in use.")
                else:
                    raise

execv("./rnmupdater.exe", ["./rnmupdater.exe"])
