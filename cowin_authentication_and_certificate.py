import json
import requests
import hashlib
# add your user agent here
browser_header = {'User-Agent':'<your user agent>'}

def generate_otp(mno):
    url='https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP'
    data = '{"mobile":"'+str(mno)+'"}'
    res= requests.post(url,  headers=browser_header, data=data)
    if(res.status_code==200):
        print('generated_otp_successfully')
    else:
        print('Error_in_otp_generation')

    return(res)


def confirm_otp(res):
    idd=res.json()['txnId']
    code = hashlib.sha256()
    code.update(input('otp:  ').encode())
    otp=code.hexdigest()
    url='https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP'
    data='{"otp": "'+ str(otp)+'","txnId": "'+str(idd)+'"}'
    res= requests.post(url,  headers=browser_header, data=data)
    if(res.status_code==200):
        print('confirm_otp_successfully')
    else:
        print('Error_in_otp_confirmation')
    return(res)


def get_certificate(res):
    beneficiary_reference_id=input('reference id')
    md=res.json()
    md1=browser_header
    md1["Authorization"] = "Bearer {}".format(md['token'])
    md1['accept']='pdf'
    url='https://cdn-api.co-vin.in/api/v2/registration/certificate/public/download'
    data={'beneficiary_reference_id':beneficiary_reference_id}
    res=requests.get(url,headers=md1,params=data)
    if(res.status_code==200):
        print('fatched_successfully')
    else:
        print('Error_in_fetching_certificate')
    return res


def generate_certificate(res):
    with open("my_file.txt", "wb") as binary_file:
        binary_file.write(res.content)
    with open('certificate.pdf', 'wb') as file:
        for line in open('my_file.txt', 'rb').readlines():
            file.write(line)

response=generate_otp(input('mno'))
response=confirm_otp(response)
response=get_certificate(response)
response=generate_certificate(response)
