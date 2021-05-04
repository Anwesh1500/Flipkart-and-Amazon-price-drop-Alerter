import streamlit as st
import requests
import smtplib
from bs4 import BeautifulSoup
import time


def alerter(receiveremail_id,al_price,url):
  headers={
    'authority': 'www.amazon.in',
    'cache-control': 'max-age=0',
    'rtt': '200',
    'downlink': '3.6',
    'ect': '4g',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.in/b?node=21505763031&pf_rd_r=R44SN4FMAJNWRK6TGT3G&pf_rd_p=f3f5d421-d316-491f-97a9-919ca1fb8ff7&pd_rd_r=73c341ca-d9d4-4f75-a713-deae31abcde2&pd_rd_w=tQT3y&pd_rd_wg=Ssapp&ref_=pd_gw_unk',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,kn;q=0.6',
    'cookie': 'session-id=257-3132020-4768019; ubid-acbin=259-2735803-8851537; ext_name=ojplmecpdpgccookcobabopnaifgidhf; i18n-prefs=INR; lc-acbin=en_IN; session-token=Mvb12GQrZaIDxO0Q0tIfe9mHJuBxYxX9h8waR0nw6ixE/17nbKv4DO0XNRQ4bs926OFTK9HVGlEZVD2jy+zjNTpHAvLDvP4wYsCiRjC7jAEZVLebKCC/+pETeBsNfMkTHRfk3cRl36Ot7VRNHXkwrn2giYCZ8HqFV9il1DcP1Os41IHWCGbU2FY7IukN1CIH; session-id-time=2082758401l; visitCount=13; csm-hit=tb:R44SN4FMAJNWRK6TGT3G+s-8MMHYNEM3M46Z409WGHW^|1620017141933&t:1620017141933&adb:adblk_no',
  }



  def sendmail(product_name,price,url,receiveremail_id):
    product_name=product_name
    price=price
    url=url
    receiveremail_id=receiveremail_id

    try:
      smtpobj = smtplib.SMTP('smtp.mail.yahoo.com', 587)

      smtpobj.starttls()
      senderemail_id="sender@yahoo.com"
      senderemail_id_password="###########"         #Enter the app password of sender email

      smtpobj.login(senderemail_id, senderemail_id_password)

      message = "Subject:Hey the Price of %s has been Dropped \n\nThe price has been dropped to %d click on the below link to go to the product page\n"%(product_name,price)
      message+='Go to the page:'+url

      smtpobj.sendmail(senderemail_id,receiveremail_id, message.encode('utf-8'))

      smtpobj.quit()
      st.success("The mail will be sent when the price of the product gets dropped to your set value")
    except:
      st.Error("Error: unable to send email Please check your mail address")


  


  def getprice_flipkart(url,receiveremail_id):
    while True:
      price=(soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text())
      price=price.replace(',','')
      price=price.replace('₹','')
      price=int(price)
      product_name=soup.find('span',{'class':'B_NuCI'}).get_text()

      if price<=al_price:
        sendmail(product_name,price,url,receiveremail_id)
      else:
        pass

      time.sleep(60*60)  

  def getprice_amazon(url,receiveremail_id):
    while True:
      try:
        price=soup.find('span',attrs={'class':'a-size-medium a-color-price priceBlockDealPriceString'}).get_text()
        price=price.replace('₹','')
        price=price.replace(',','')
        ind=price.index('.')
        price=int(price[:ind])
        product_name=soup.find('span',attrs={'class':'a-size-large product-title-word-break'}).get_text()
        product_name=product_name.strip()
      except:
        price=soup.find('span',attrs={'class':'a-size-medium a-color-price priceBlockSalePriceString'}).get_text()
        price=price.replace('₹','')
        price=price.replace(',','')
        ind=price.index('.')
        price=int(price[:ind])
        product_name=soup.find('span',attrs={'class':'a-size-large product-title-word-break'}).get_text()
        product_name=product_name.strip()
  
      if price<=al_price:
        sendmail(product_name,price,url,receiveremail_id)
      else:
        pass

      time.sleep(60*60)

  
  
  al_price=int(al_price)
  page=requests.get(url,headers=headers)
  soup=BeautifulSoup(page.content,'html.parser')
  if url.startswith('https://www.flipkart.com'):
    getprice_flipkart(url,receiveremail_id)
  elif url.startswith('https://www.amazon.in'):
    getprice_amazon(url,receiveremail_id)  




st.title('Price Drop Alerter')
st.header("Enter the URL of the Product ")
url=st.text_input('')
if st.button("OK"):
  st.success("Product URL Entered Successfully")

st.header("Enter Email id to get Notified ")
receiveremail_id=st.text_input(' ')
if st.button('SUBMIT'):
  st.success(f"Entered email address is {receiveremail_id}")

st.sidebar.header("Enter the expected price dropped value")
al_price=st.sidebar.number_input('')
st.sidebar.slider("Entered Price is",al_price-1000.0,al_price+1000.0,al_price)

if st.sidebar.button("Set Price"):
  st.sidebar.success(f"The price set by you is {al_price}")

if al_price==0.00:
  st.warning("The Price field is empty")

if st.button("GET ALERTED"):
  alerter(receiveremail_id,al_price,url)
