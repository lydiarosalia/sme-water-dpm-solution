# ----- Create function that is triggered by http request
def importDataHmw(request):
    # ----- Import libraries
    from google.cloud import storage
    from urllib import request

    # ----- Set storage client
    client2 = storage.Client()

    # ----- Get bucket
    bucket = client2.get_bucket('raw-data-import-hmw')  # without gs://
    blob = bucket.blob('test.csv')

    # ----- Copy file to google storage
    ftpfile = request.urlopen(
        'https://st.hwmonline.com/hwmonline/hwmcarcgi.cgi?user=viewer01&pass=viewer01&logger=35619&startdate=2019-11-01+00:00&enddate=2019-11-30+23:45&flowunits=2&pressureunits=1&flowinterval=2&interval=5&export=csv')
    blob.upload_from_file(ftpfile)
    print('File copied to google storage')


