echo "Waiting for rodnmod process to stop in order to proceed updating! Please do not close this window."
while pgrep -x "rodnmod" > /dev/null; do
    echo "Rodnmod is still running. Checking again in 5 seconds..."
    sleep 5
done
echo "Rodnmod has stopped. Proceeding with update."

7z x update.7z -y
rm -f update.7z
./rodnmod