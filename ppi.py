#Developer: Curly60e
#PyBLOCK its a clock of the Bitcoin blockchain.
#Version: 0.5.0

import base64, codecs, json, requests
import pickle
import os
import os.path
import qrcode
import lnpay_py
import requests
import simplejson as json
import time as t
from art import *
from pblogo import *
from logos import *
from lnpay_py.wallet import LNPayWallet

def clear(): # clear the screen
    os.system('cls' if os.name=='nt' else 'clear')

#-----------------------------LNBITS--------------------------------

def loadFileConnLNBits(lnbitLoad):
    lnbitLoad = {"wallet_name":"", "wallet_id":"", "admin_key":"", "invoice_read_key":""}

    if os.path.isfile('lnbit.conf'): # Check if the file 'bclock.conf' is in the same folder
        lnbitData= pickle.load(open("lnbit.conf", "rb")) # Load the file 'bclock.conf'
        lnbitLoad = lnbitData # Copy the variable pathv to 'path'
    else:
        clear()
        blogo()
        print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO LNBITS.COM.
                   WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                          IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                           SAVE THE FILE '\033[1;33;40mlnbitSN.conf\033[0;37;40m' IN A SAFE PLACE.\n
        """)
        lnbitLoad["wallet_name"] = input("Wallet name: ") # path to the bitcoin-cli
        lnbitLoad["wallet_id"] = input("Wallet ID: ")
        lnbitLoad["admin_key"] = input("Admin key: ")
        lnbitLoad["invoice_read_key"] = input("Invoice/read key: ")
        pickle.dump(lnbitLoad, open("lnbit.conf", "wb"))
    return lnbitLoad

def createFileConnLNBits():
    lnbitLoad = {"wallet_name":"", "wallet_id":"", "admin_key":"", "invoice_read_key":""}

    clear()
    blogo()
    print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO LNBITS.COM.
               WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                      IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                       SAVE THE FILE '\033[1;33;40mlnbitSN.conf\033[0;37;40m' IN A SAFE PLACE.\n
    """)
    lnbitLoad["wallet_name"] = input("Wallet name: ") # path to the bitcoin-cli
    lnbitLoad["wallet_id"] = input("Wallet ID: ")
    lnbitLoad["admin_key"] = input("Admin key: ")
    lnbitLoad["invoice_read_key"] = input("Invoice/read key: ")

    pickle.dump(lnbitLoad, open("lnbit.conf", "wb"))

def lnbitCreateNewInvoice():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    try:
        print("\n\tLNBITS CREATE INVOICE\n")
        amt = input("Amount: ")
        memo = input("Memo: ")
        a = loadFileConnLNBits(['invoice_read_key'])
        b = str(a['invoice_read_key'])
        curl = 'curl -X POST https://lnbits.com/api/v1/payments -d ' + "'{" + """"out": false, "amount": {}, "memo": "{} -PyBLOCK" """.format(amt,memo) + "}'" + """ -H "X-Api-Key: {} " -H "Content-type: application/json" """.format(b)
        sh = os.popen(curl).read()
        clear()
        blogo()
        n = str(sh)
        d = json.loads(n)
        q = d['payment_request']
        c = q.lower()
        while True:
            print("\033[1;30;47m")
            qr.add_data(c)
            qr.print_ascii()
            print("\033[0;37;40m")
            qr.clear()
            print("Lightning Invoice: " + c)
            t.sleep(10)
            dn = str(d['checking_id'])
            checkcurl = 'curl -X GET https://lnbits.com/api/v1/payments/' + dn + """ -H "X-Api-Key: {}" -H "Content-type: application/json" """.format(b)
            rsh = os.popen(checkcurl).read()
            clear()
            blogo()
            nn = str(rsh)
            dd = json.loads(nn)
            db = dd['paid']
            if db == True:
                clear()
                blogo()
                tick()
                t.sleep(2)
                break
            else:
                continue
    except:
        pass


def lnbitPayInvoice():
    bolt = input("Invoice: ")
    a = loadFileConnLNBits(['admin_key'])
    b = str(a['admin_key'])
    curl = 'curl -X POST https://lnbits.com/api/v1/payments -d ' + "'{" + """"out": true, "bolt11": "{}" """.format(bolt) + "}'" + """ -H "X-Api-Key: {}" -H "Content-type: application/json" """.format(b)
    try:
        sh = os.popen(curl).read()
        n = str(sh)
        d = json.loads(n)
        dn = str(d['checking_id'])
        a = loadFileConnLNBits(['invoice_read_key'])
        b = str(a['invoice_read_key'])
        while True:
            checkcurl = 'curl -X GET https://lnbits.com/api/v1/payments/' + dn + """ -H "X-Api-Key: {}" -H "Content-type: application/json" """.format(b)
            rsh = os.popen(checkcurl).read()
            clear()
            blogo()
            nn = str(rsh)
            dd = json.loads(nn)
            db = dd['paid']
            if db == True:
                tick()
                t.sleep(2)
                break
            else:
                continue
    except:
        pass

def lnbitCreatePayWall():
    while True:
        try:
            url = input("Url: ")
            memo = input("Memo: ")
            desc = input("Description: ")
            amt = input("Amount in sats: ")
            remb = input("Remembers Y/n: ")
            a = loadFileConnLNBits(['admin_key'])
            b = str(a['admin_key'])
            if remb in ["Y", "y"]:
                remember = "true"
            elif remb in ["N", "n"]:
                remember = "false"
            curl = 'curl -X POST https://lnbits.com/paywall/api/v1/paywalls -d ' + "'{" + """"url": "{}", "memo": "{}", "description": "{}", "amount": {}, "remembers": {} """.format(url,memo,desc,amt,remember) + "}'" + """ -H  "Content-type: application/json" -H "X-Api-Key: {}" """.format(b)
            sh = os.popen(curl).read()
            clear()
            blogo()
            n = str(sh)
            d = json.loads(n)
            print("\n\tPAYWALL CREATED SUCCESSFULLY\n")
            t.sleep(2)
            clear()
            aa = loadFileConnLNBits(['invoice_read_key'])
            bb = str(a['invoice_read_key'])
            checkcurl = 'curl -X GET https://lnbits.com/paywall/api/v1/paywalls -H' + """ "X-Api-Key: {}" """.format(bb)
            sh = os.popen(checkcurl).read()
            clear()
            blogo()
            n = str(sh)
            d = json.loads(n)
            while True:
                print("\n\tLNBITS PAYWALL LIST\n")
                for r in range(len(d)):
                    s = d[r]
                    print("ID: " + s['id'])
                nd = input("\nSelect ID: ")
                for r in range(len(d)):
                    s = d[r]
                    nn = s['id']
                    if nd == nn:
                        print("\n----------------------------------------------------------------------------------------------------------------")
                        print("""
                        \tLNBITS PAYWALL DECODED

                        ID: {}
                        Amount: {} sats
                        Description: {}
                        Memo: {}
                        Extras: {}
                        Remembers: {}
                        URL: {}
                        Wallet: {}
                        """.format(s['id'], s['amount'], s['description'], s['memo'], s['extras'], s['remembers'], s['url'], s['wallet']))
                        print("----------------------------------------------------------------------------------------------------------------\n")
                input("Continue...")
            clear()
            blogo()
        except:
            break

def lnbitListPawWall():
    a = loadFileConnLNBits(['invoice_read_key'])
    b = str(a['invoice_read_key'])
    checkcurl = 'curl -X GET https://lnbits.com/paywall/api/v1/paywalls -H' + """ "X-Api-Key: {}" """.format(b)
    sh = os.popen(checkcurl).read()
    clear()
    blogo()
    n = str(sh)
    d = json.loads(n)
    while True:
        print("\n\tLNBITS PAYWALL LIST\n")
        try:
            for item_ in d:
                s = item_
                print("ID: " + s['id'])
            nd = input("\nSelect ID: ")
            for item in d:
                s = item
                nn = s['id']
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------------------")
                    print("""
                    \tLNBITS PAYWALL DECODED

                    ID: {}
                    Amount: {} sats
                    Description: {}
                    Memo: {}
                    Extras: {}
                    Remembers: {}
                    URL: {}
                    Wallet: {}
                    """.format(s['id'], s['amount'], s['description'], s['memo'], s['extras'], s['remembers'], s['url'], s['wallet']))
                    print("----------------------------------------------------------------------------------------------------------------\n")
        except:
            break
        input("Continue...")
        clear()
        blogo()


def lnbitDeletePayWall():
    while True:
        try:
            a = loadFileConnLNBits(['invoice_read_key'])
            b = str(a['invoice_read_key'])
            checkcurl = 'curl -X GET https://lnbits.com/paywall/api/v1/paywalls -H' + """ "X-Api-Key: {}" """.format(b)
            sh = os.popen(checkcurl).read()
            clear()
            blogo()
            n = str(sh)
            d = json.loads(n)
            while True:
                print("\n\tLNBITS PAYWALL LIST\n")
                try:
                    for item_ in d:
                        s = item_
                        print("ID: " + s['id'])
                    nd = input("\nSelect ID: ")
                    for item in d:
                        s = item
                        nn = s['id']
                        if nd == nn:
                            print("\n----------------------------------------------------------------------------------------------------------------")
                            print("""
                            \tLNBITS PAYWALL DECODED

                            ID: {}
                            Amount: {} sats
                            Description: {}
                            Memo: {}
                            Extras: {}
                            Remembers: {}
                            URL: {}
                            Wallet: {}
                            """.format(s['id'], s['amount'], s['description'], s['memo'], s['extras'], s['remembers'], s['url'], s['wallet']))
                            print("----------------------------------------------------------------------------------------------------------------\n")
                except:
                    break
                input("Continue...")
                break
            print("\n\tDELETE PAYWALL\n")
            a = loadFileConnLNBits(['admin_key'])
            b = str(a['admin_key'])
            id = input("Insert PayWall ID: ")
            curl = "curl -X DELETE https://lnbits.com/paywall/api/v1/paywalls/{}".format(id) + """ -H "X-Api-Key: {}" """.format(b)
            sh = os.popen(curl).read()
            clear()
            blogo()
            print("\n\tPAYWALL DELETED SUCCESSFULLY\n")
            t.sleep(2)
            clear()
        except:
            break

#-----------------------------END LNBITS--------------------------------

#-----------------------------LNPAY--------------------------------
def loadFileConnLNPay(lnpayLoad):
    lnpayLoad = {"key":""}

    if os.path.isfile('lnpay.conf'): # Check if the file 'bclock.conf' is in the same folder
        lnpayData= pickle.load(open("lnpay.conf", "rb")) # Load the file 'bclock.conf'
        lnpayLoad = lnpayData # Copy the variable pathv to 'path'
    else:
        clear()
        blogo()
        print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO LNPAY.CO.
                   WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                          IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                           SAVE THE FILE '\033[1;33;40mlnpaySN.conf\033[0;37;40m' IN A SAFE PLACE.\n
        """)
        lnpayLoad["key"] = input("API Key: ")
        print("\n\tWALLET ACCESS KEYS\n")
        lnpayLoad["wallet_key_id"] = input("Wallet Admin: ")
        pickle.dump(lnpayLoad, open("lnpay.conf", "wb"))
    clear()
    blogo()
    return lnpayLoad

def createFileConnLNPay():
    clear()
    blogo()
    print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO LNPAY.CO.
               WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                      IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                       SAVE THE FILE '\033[1;33;40mlnpaySN.conf\033[0;37;40m' IN A SAFE PLACE.\n
    """)
    lnpayLoad["key"] = input("API Key: ")
    print("\n\tWALLET ACCESS KEYS\n")
    lnpayLoad["wallet_key_id"] = input("Wallet Admin: ")
    pickle.dump(lnpayLoad, open("lnpay.conf", "wb"))


def lnpayGetBalance():
    a = loadFileConnLNPay(['key'])
    b = str(a['key'])
    n = loadFileConnLNPay(['wallet_key_id'])
    q = str(n['wallet_key_id'])
    lnpay_py.initialize(b)
    clear()
    blogo()
    my_wallet = LNPayWallet(q)
    info = my_wallet.get_info()
    print("\n---------------------------------------------------------------------------------------------------")
    print("""
    \tLNPAY WALLET BALANCE

    Wallet ID: {}
    Wallet Name: {}
    Balance: {} sats
    """.format(info['id'], info['user_label'], info['balance']))
    print("---------------------------------------------------------------------------------------------------\n")
    input("\nContinue... ")

def lnpayCreateInvoice():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    a = loadFileConnLNPay(['key'])
    b = str(a['key'])
    n = loadFileConnLNPay(['wallet_key_id'])
    q = str(n['wallet_key_id'])
    lnpay_py.initialize(b)
    clear()
    blogo()
    my_wallet = LNPayWallet(q)
    amt = input("\nAmount in Sats: ")
    memo = input("Memo: ")
    invoice_params = {
        'num_satoshis': amt,
        'memo': memo + ' -PyBLOCK'
    }
    try:
        invoice = my_wallet.create_invoice(invoice_params)
        while True:
            print("\033[1;30;47m")
            qr.add_data(invoice['payment_request'])
            qr.print_ascii()
            print("\033[0;37;40m")
            qr.clear()
            print("Lightning Invoice: " + invoice['payment_request'])
            t.sleep(10)
            curl = 'curl -u ' + b + ': https://lnpay.co/v1/lntx/' + invoice['id'] + '?fields=settled,num_satoshis'
            rsh = os.popen(curl).read()
            clear()
            blogo()
            nn = str(rsh)
            dd = json.loads(nn)
            db = dd['settled']
            if db == 1:
                clear()
                blogo()
                tick()
                t.sleep(2)
                break
            else:
                continue
    except:
        pass


def lnpayGetTransactions():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    a = loadFileConnLNPay(['key'])
    b = str(a['key'])
    n = loadFileConnLNPay(['wallet_key_id'])
    q = str(n['wallet_key_id'])
    lnpay_py.initialize(b)
    clear()
    blogo()
    my_wallet = LNPayWallet(q)

    transactions = my_wallet.get_transactions()
    while True:
        try:
            print("\n\tLNPAY LIST PAYMENTS\n")
            for transaction_ in transactions:
                s = transaction_
                q = s['lnTx']

                print("ID: " + s['id'])
            nd = input("\nSelect ID: ")
            for transaction in transactions:
                s = transaction
                nn = s['id']
                nnn = s['lnTx']
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------")
                    print("""
                    \tLNPAY LIST PAYMENT DECODED

                    ID: {}
                    Amount: {} sats
                    Memo: {}
                    Invoice: {}
                    RHash: {}
                    """.format(nnn['id'], nnn['num_satoshis'], nnn['memo'], nnn['payment_request'], nnn['r_hash_decoded']))
                    print("----------------------------------------------------------------------------------------------------\n")
                    print("\033[1;30;47m")
                    qr.add_data(nnn['payment_request'])
                    qr.print_ascii()
                    print("\033[0;37;40m")
                    qr.clear()
            input("Continue...")
            clear()
            blogo()
        except:
            break
    clear()
    blogo()

def lnpayPayInvoice():
    a = loadFileConnLNPay(['key'])
    b = str(a['key'])
    n = loadFileConnLNPay(['wallet_key_id'])
    q = str(n['wallet_key_id'])
    lnpay_py.initialize(b)
    clear()
    blogo()
    my_wallet = LNPayWallet(q)
    try:
        print("\n\tLNPAY PAY INVOICE\n")
        inv = input("\nInvoice: ")
        curl = 'curl -u' + b +': https://lnpay.co/v1/node/default/payments/decodeinvoice?payment_request=' + inv
        clear()
        rsh = os.popen(curl).read()
        nn = str(rsh)
        dd = json.loads(nn)
        clear()
        blogo()
        print("\n----------------------------------------------------------------------------------------------------")
        print("""
        \tLNPAY INVOICE DECODED

        Destination: {}
        Amount: {} sats
        Memo: {}
        Invoice: {}
        """.format(dd['destination'], dd['num_satoshis'], dd['description'], inv))
        print("----------------------------------------------------------------------------------------------------\n")
        print("<<< Cancel Control + C")
        input("\nEnter to Continue... ")
        invoice_params = {
            'payment_request': inv
        }
        pay_result = my_wallet.pay_invoice(invoice_params)
    except:
        pass

def lnpayTransBWallets():
    a = loadFileConnLNPay(['key'])
    b = str(a['key'])
    n = loadFileConnLNPay(['wallet_key_id'])
    q = str(n['wallet_key_id'])
    lnpay_py.initialize(b)
    clear()
    blogo()
    print("""\n\tLNPAY TRANSFER BETWEEN WALLETS
    \nCaution: If you Transfer to another of your LNPay wallets
    you will only access to your funds via Web.\n""")
    try:
        wall = input("Wallet destination ID: ")
        amt = input("Amount in Sats: ")
        memo = input("Memo: ")
        my_wallet = LNPayWallet(q)
        transfer_params = {
            'dest_wallet_id': wall,
            'num_satoshis': amt,
            'memo': memo
        }
        transfer_result = my_wallet.internal_transfer(transfer_params)
        p = transfer_result['wtx_transfer_in']
        e = transfer_result['wtx_transfer_out']
        f = e['wal']
        v = p['wal']
        print("\n----------------------------------------------------------------------------------------------------")
        print("""
        \tLNPAY TRANSFER BETEWWN WALLETS INFORMATION

        ID: {}
        Amount: {} sats
        Memo: {}
        To Wallet: {}
        From Wallet: {}
        """.format(p['id'], p['num_satoshis'], p['user_label'], v['user_label'], f['user_label']))
        print("----------------------------------------------------------------------------------------------------\n")
        input("Continue...")
    except:
        pass


#-----------------------------END LNPAY--------------------------------

#-----------------------------OPENNODE--------------------------------

def loadFileConnOpenNode(opennodeLoad):
    opennodeLoad = {"key":"","wdr":"","inv":""}

    if os.path.isfile('opennode.conf'): # Check if the file 'bclock.conf' is in the same folder
        opennodeData= pickle.load(open("opennode.conf", "rb")) # Load the file 'bclock.conf'
        opennodeLoad = opennodeData # Copy the variable pathv to 'path'
    else:
        clear()
        blogo()
        print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO OPENNODE.COM.
                   WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                          IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                           SAVE THE FILE '\033[1;33;40mopennodeSN.conf\033[0;37;40m' IN A SAFE PLACE.\n
        """)
        opennodeLoad["key"] = input("API Read Only Key: ")
        opennodeLoad["wdr"] = input("API Withdrawall Key: ")
        opennodeLoad["inv"] = input("API Invoices Key: ")
        pickle.dump(opennodeLoad, open("opennode.conf", "wb"))
    clear()
    blogo()
    return opennodeLoad

def createFileConnOpenNode():
    opennodeLoad = {"key":"","wdr":"","inv":""}

    clear()
    blogo()
    print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO OPENNODE.COM.
               WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                      IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                       SAVE THE FILE '\033[1;33;40mopennodeSN.conf\033[0;37;40m' IN A SAFE PLACE.\n
    """)
    opennodeLoad["key"] = input("API Read Only Key: ")
    opennodeLoad["wdr"] = input("API Withdrawall Key: ")
    opennodeLoad["inv"] = input("API Invoices Key: ")
    pickle.dump(opennodeLoad, open("opennode.conf", "wb"))

def OpenNodelistfunds():
    a = loadFileConnOpenNode(['wdr'])
    b = str(a['wdr'])
    curl = "curl https://api.opennode.co/v1/account/balance -H "+ '"Content-Type: application/json" -H "Authorization: {}"'.format(b)
    sh = os.popen(curl).read()
    clear()
    blogo()
    n = str(sh)
    d = json.loads(n)
    r = d['data']
    p = r['balance']
    print("\n----------------------------------------------------------------------------------------------------")
    print("""
    OPENNODE BALANCE

    Amount: {} sats
    """.format(p['BTC']))
    print("----------------------------------------------------------------------------------------------------\n")
    input("Continue...")

def OpenNodecreatecharge():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    a = loadFileConnOpenNode(['key'])
    b = str(a['key'])
    fiat = input("Are you going to pay in FIAT? Y/n:")
    if fiat in ["Y", "y"]:
        print("\n----------------------------------------------------------------------------------------------------")
        print("""
        \tFIAT supported on OpenNode:

        AED,AFN,ALL,AMD,ANG,AOA,ARS,AUD,AWG,AZN,BAM,BBD,BDT,BGN,BHD,BIF,BMD,BND,BOB,BRL,BSD,BTN,BWP,
        BYN,BZD,CAD,CDF,CHF,CLF,CLP,CNH,CNY,COP,CRC,CUC,CUP,CVE,CZK,DJF,DKK,DOP,DZD,EGP,ERN,ETB,EUR,
        FJD,FKP,GBP,GEL,GGP,GHS,GIP,GMD,GNF,GTQ,GYD,HKD,HNL,HRK,HTG,HUF,IDR,ILS,IMP,INR,IQD,IRR,ISK,
        JEP,JMD,JOD,JPY,KES,KGS,KHR,KMF,KPW,KRW,KWD,KYD,KZT,LAK,LBP,LKR,LRD,LSL,LYD,MAD,MDL,MGA,MKD,
        MMK,MNT,MOP,MRO,MUR,MVR,MWK,MXN,MYR,MZN,NAD,NGN,NIO,NOK,NPR,NZD,OMR,PAB,PEN,PGK,PHP,PKR,PLN,
        PYG,QAR,RON,RSD,RUB,RWF,SAR,SBD,SCR,SDG,SEK,SGD,SHP,SLL,SOS,SRD,SSP,STD,SVC,SYP,SZL,THB,TJS,
        TMT,TND,TOP,TRY,TTD,TWD,TZS,UAH,UGX,USD,UYU,UZS,VES,VND,VUV,WST,XAF,XAG,XAU,XCD,XDR,XOF,XPD,
        XPF,XPT,YER,ZAR,ZMW,ZWL,USDC.
        """)
        print("\n----------------------------------------------------------------------------------------------------")
        selection = input("Select a FIAT currency: ")
        amt = input("Amount in {}: ".format(selection))
        curl = 'curl https://api.opennode.co/v1/charges -X POST -H ' + '"Authorization: {}"'.format(b) + ' -H "Content-Type: application/json" -d ' + "'{" + '"amount": "{}", "currency": "{}"'.format(amt,selection.upper()) +  "}'"
        sh = os.popen(curl).read()
        clear()
        blogo()
        n = str(sh)
        d = json.loads(n)
        dd = d['data']
        qq = dd['lightning_invoice']
        pp = dd['chain_invoice']
        nn = qq['payreq']
        mm = nn.lower()
        while True:
            try:
                print("\n----------------------------------------------------------------------------------------------------")
                print("""
                \tOPENNODE PAYMENT REQUEST

                Amount: {} {}
                ID: {}
                Status: {}
                Invoice: {}
                Onchain Address: {}
                Amount: {} sats
                """.format(amt, selection.upper(), dd['id'], dd['status'], mm, pp['address'], dd['amount']))
                print("----------------------------------------------------------------------------------------------------\n")
                p = pp['address']
                pay = input("Invoice or Onchain Address? I/O: ")
                if pay =="I" or pay == "i":
                    print("\033[1;30;47m")
                    qr.add_data(mm)
                    qr.print_ascii()
                    print("\033[0;37;40m")
                    qr.clear()
                    print("\nLightning Invoice: " + mm)
                elif pay =="O" or pay == "o":
                    print("\033[1;30;47m")
                    qr.add_data(p)
                    qr.print_ascii()
                    print("\033[0;37;40m")
                    qr.clear()
                    print("\nAmount in sats: {} sats".format(dd['amount']))
                    print("\nOnchain Address: " + p)
                input("\nContinue...")
                clear()
                blogo()
            except:
                break
    elif fiat == "N" or fiat == "n":
        amt = input("Amount in sats: ")
        curl = 'curl https://api.opennode.co/v1/charges -X POST -H' + '"Authorization: {}"'.format(b) + ' -H "Content-Type: application/json" -d ' + "'{" + '"amount": "{}", "currency": "BTC"'.format(amt) +  "}'"
        sh = os.popen(curl).read()
        clear()
        blogo()
        n = str(sh)
        d = json.loads(n)
        dd = d['data']
        qq = dd['lightning_invoice']
        pp = dd['chain_invoice']
        nn = qq['payreq']
        mm = nn.lower()
        while True:
            try:
                print("\n----------------------------------------------------------------------------------------------------")
                print("""
                \tOPENNODE PAYMENT REQUEST

                Amount: {} sats
                ID: {}
                Status: {}
                Invoice: {}
                Onchain Address: {}
                Amount: {} sats
                """.format(amt, dd['id'], dd['status'], mm, pp['address'], dd['amount']))
                print("----------------------------------------------------------------------------------------------------\n")
                p = pp['address']
                pay = input("Invoice or Onchain Address? I/O: ")
                if pay =="I" or pay == "i":
                    print("\033[1;30;47m")
                    qr.add_data(mm)
                    qr.print_ascii()
                    print("\033[0;37;40m")
                    qr.clear()
                    print("\nLightning Invoice: " + mm)
                elif pay =="O" or pay == "o":
                    print("\033[1;30;47m")
                    qr.add_data(p)
                    qr.print_ascii()
                    print("\033[0;37;40m")
                    qr.clear()
                    print("\nAmount in sats: {} sats".format(dd['amount']))
                    print("\nOnchain Address: " + p)
                input("\nContinue...")
                clear()
                blogo()
            except:
                break


def OpenNodeiniciatewithdrawal():
    a = loadFileConnOpenNode(['wdr'])
    b = str(a['wdr'])
    c = loadFileConnOpenNode(['key'])
    d = str(a['key'])
    lnchain = input("Are you going to pay with Lightning or Onchain? L/O: ")
    clear()
    blogo()
    if lnchain in ["L", "l"]:
        try:
            while True:
                invoice = input("\nInvoice: ")
                checkcurl = 'curl https://api.opennode.co/v1/charge/decode -X POST -H "Authorization: {}" -H "Content-Type: application/json" -d '.format(b) + "'{" + '"pay_req": "{}"'.format(invoice) + "}'"
                ssh = os.popen(checkcurl).read()
                nn = str(ssh)
                dd = json.loads(nn)
                print(dd)
                if invoice == "":
                    print("\n----------------------------------------------------------------------------------------------------")
                    print("""
                    \tOPENNODE TRANSFER REQUEST

                    Message: {}
                    """.format(dd['message']))
                    print("----------------------------------------------------------------------------------------------------\n")
                else:
                    break
            rr = dd['data']
            ss = rr['pay_req']

            print("\n----------------------------------------------------------------------------------------------------")
            print("""
            \tOPENNODE TRANSFER REQUEST

            Network: {}
            Amount: {} sats
            Destination: {}
            Hash: {}
            """.format(ss['network'],ss['amount'],ss['pub_key'],ss['hash']))
            print("----------------------------------------------------------------------------------------------------\n")
            print("<<< Cancel Control + C")
            input("\nEnter to Continue... ")

            curl = 'curl https://api.opennode.co/v2/withdrawals -X POST -H "Content-Type: application/json" -H "Authorization: {}"'.format(b) + " -d '{" + '"type": "ln", "address": "{}", "callback_url": ""'.format(invoice) + "}'"
            sh = os.popen(curl).read()
            n = str(sh)
            d = json.loads(n)
            clear()
            blogo()
            tick()
            t.sleep(2)
        except:
            pass

    elif lnchain == "O" or lnchain == "o":
        try:
            while True:
                print("\n\tOPENNODE TRANSFER REQUEST\n")
                print("\n\tMinimum amount 200000 sats\n")
                address = input("\nBitcoin Address: ")
                amt = int(input("Amount in sats: "))
                curl = 'curl https://api.opennode.co/v2/withdrawals -X POST -H "Content-Type: application/json" -H "Authorization: {}"'.format(b) + " -d '{" + '"type": "chain", "amount": {}, "address": "{}", "callback_url": ""'.format(amt,address) + "}'"
                if amt < 199999:
                    sh = os.popen(curl).read()
                    n = str(sh)
                    d = json.loads(n)
                    print("\n----------------------------------------------------------------------------------------------------")
                    print("""
                    \tOPENNODE TRANSFER REQUEST

                    Message: {}
                    """.format(d['message']))
                    print("----------------------------------------------------------------------------------------------------\n")
                elif amt > 200000:
                    sh = os.popen(curl).read()
                    n = str(sh)
                    d = json.loads(n)
                    dd = d['data']
                    print("\n----------------------------------------------------------------------------------------------------")
                    print("""
                    \tOPENNODE TRANSFER REQUEST

                    Amount: {} sats
                    Address Destination: {}
                    Fee: {}
                    Status: {}
                    """.format(dd['amount'],dd['address'],dd['fee'], dd['status']))
                    print("----------------------------------------------------------------------------------------------------\n")
                    input("\nContinue... ")
                    clear()
                    blogo()
                    logoB()
                    t.sleep(2)
                    break
        except:
            pass

def OpenNodeListPayments():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    a = loadFileConnOpenNode(['wdr'])
    b = str(a['wdr'])
    curl = 'curl https://api.opennode.co/v1/withdrawals -H "Content-Type: application/json" -H "Authorization: {}"'.format(b)
    sh = os.popen(curl).read()
    clear()
    blogo()
    print("\n\tOPENNODE TRANSACTIONS LIST\n")
    n = str(sh)
    d = json.loads(n)
    da = d['data']
    while True:
        try:
            for item_ in da:
                s = item_
                n = s['status']
                q = str(n)
                print("ID: " + s['id'] + " " + q)
            nd = input("\nSelect ID: ")
            for item in da:
                s = item
                nn = s['id']
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------")
                    print("""
                    \tOPENNODE TRANSACTION DECODED
                    ID: {}
                    Amount: {} sats
                    Type: {}
                    Invoice or Tx ID: {}
                    Status: {}
                    """.format(s['id'], s['amount'], s['type'], s['reference'], s['status']))
                    print("----------------------------------------------------------------------------------------------------\n")
                    print("\033[1;30;47m")
                    qr.add_data(s['reference'])
                    qr.print_ascii()
                    print("\033[0;37;40m")
                    qr.clear()
            input("Continue...")
            clear()
            blogo()
            print("\n\tOPENNODE TRANSACTIONS LIST\n")
        except:
            break
#-----------------------------END OPENNODE--------------------------------

#-----------------------------TIPPINME--------------------------------

def loadFileTippinMe(tippinmeLoad):
    tippinmeLoad = {"key":""}

    if os.path.isfile('tippinme.conf'): # Check if the file 'bclock.conf' is in the same folder
        tippinmeData= pickle.load(open("tippinme.conf", "rb")) # Load the file 'bclock.conf'
        tippinmeLoad = tippinmeData # Copy the variable pathv to 'path'
    else:
        clear()
        blogo()
        print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOUR CONFIGURATION INFORMATION WILL BE SAVE IN '\033[1;33;40mtippinme.conf\033[0;37;40m'
                                                                IF YOU NEED TO START AGAIN, DELETE IT.\n
        """)
        tippinmeLoad["key"] = input("Twitter @user: ")
        pickle.dump(tippinmeLoad, open("tippinme.conf", "wb"))
    clear()
    blogo()
    return tippinmeLoad

def createFileTippinMe():
    tippinmeLoad = {"key":""}
    clear()
    blogo()
    print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOUR CONFIGURATION INFORMATION WILL BE SAVE IN '\033[1;33;40mtippinme.conf\033[0;37;40m'
                                                                IF YOU NEED TO START AGAIN, DELETE IT.\n
    """)
    tippinmeLoad["key"] = input("Twitter @user: ")
    pickle.dump(tippinmeLoad, open("tippinme.conf", "wb"))

def tippinmeGetInvoice():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    a = loadFileTippinMe(['key'])
    b = str(a['key'])
    try:
        print("\n\tTIPPINME GENERATE INVOICE\n")
        q = input("Amount in Sats: ")
        clear()
        blogo()
        url = 'https://api.tippin.me/v1/public/addinvoice/{}/{}'.format(b,q)
        response = requests.get(url)
        responseB = str(response.text)
        responseC = responseB
        lnreq = responseC.split(',')
        lnbc1 = lnreq[1]
        lnbc1S = str(lnbc1)
        lnbc1R = lnbc1S.split(':')
        lnbc1W = lnbc1R[1]
        ln = str(lnbc1W)
        ln1 = ln.strip('"')
        print("\033[1;30;47m")
        qr.add_data(ln1)
        qr.print_ascii()
        print("\033[0;37;40m")
        print("LND Invoice: " + ln1)
        response.close()
        input("Continue...")
    except:
        pass


#-----------------------------END TIPPINME--------------------------------


#-----------------------------LNTXBOT--------------------------------

def loadFileLNTXBOT(lntxbotLoad):
    lntxbotLoad = {"key":"", "log":""}

    if os.path.isfile('lntxbot.conf'): # Check if the file 'bclock.conf' is in the same folder
        lntxbotData= pickle.load(open("lntxbot.conf", "rb")) # Load the file 'bclock.conf'
        lntxbotLoad = lntxbotData # Copy the variable pathv to 'path'
    else:
        clear()
        blogo()
        print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO TIPPIN.ME.
                   WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                          IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                           SAVE THE FILE '\033[1;33;40mtippinmeSN.conf\033[0;37;40m' IN A SAFE PLACE.\n
        """)
        lntxbotLoad["key"] = input("Full Access API: ")
        lntxbotLoad["log"] = input("Telegram @USER: ")
        pickle.dump(lntxbotLoad, open("lntxbot.conf", "wb"))
    clear()
    blogo()
    return lntxbotLoad

def createFileLNTXBOT():
    lntxbotLoad = {"key":"", "log":""}
    clear()
    blogo()
    print("""\n\t   \033[1;33;40mATENTION\033[0;37;40m: YOU ARE GOING TO CREATE A FILE WITH YOUR INFORMATION OF CONNECTION TO TIPPIN.ME.
               WE WILL NEED SOME INFORMATION FROM YOUR ACCOUNT THAT THE ONLY ONE THAT WILL HAVE ACCESS IS YOU.
                      IF YOU DELETE THIS FILE YOU WILL NEED TO PAY AGAIN TO GET ACCESS FROM PyBLOCK.
                                       SAVE THE FILE '\033[1;33;40mtippinmeSN.conf\033[0;37;40m' IN A SAFE PLACE.\n
    """)
    lntxbotLoad["key"] = input("Full Access API: ")
    pickle.dump(lntxbotLoad, open("lntxbot.conf", "wb"))

def lntxbotGetInvoice():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    a = loadFileLNTXBOT(['key'])
    b = str(a['key'])
    c = loadFileLNTXBOT(['log'])
    d = str(c['log'])
    curl = 'curl -X GET https://lntxbot.bigsun.xyz/@{} -H'.format(d) + '"X-Api-Key: {}"'.format(b) + '-H "Content-type: application/json"'
    sh = os.popen(curl).read()
    n = str(sh)
    print(n)
    d = json.loads(n)
    print(d)
    print("\033[1;30;47m")
    qr.add_data(ln1)
    qr.print_ascii()
    print("\033[0;37;40m")
    print("LND Invoice: " + ln1)
    response.close()
    input("Continue...")

#-----------------------------END LNTXBOT--------------------------------

#-----------------------------BITNODES--------------------------------

def bitnodesListSnapshots():

    curl = 'curl -H "Accept: application/json; indent=4" https://bitnodes.io/api/v1/snapshots/'
    sh = os.popen(curl).read()
    clear()
    blogo()
    print("\n\tBITNODES SNAPSHOTS LIST\n")
    n = str(sh)
    d = json.loads(n)
    da = d['results']
    while True:
        try:
            for item_ in da:
                s = item_
                print("Timestamp: " + str(s['timestamp']))
            nd = input("\nSelect ID: ")
            for item in da:
                s = item
                nn = str(s['timestamp'])
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------")
                    print("""
                    \tBITNODES DECODED
                    URL: {}
                    Timestamp: {}
                    Total Nodes: {}
                    Latest Block Height: {}
                    """.format(s['url'], s['timestamp'], s['total_nodes'], s['latest_height']))
                    print("----------------------------------------------------------------------------------------------------\n")
            input("Continue...")
            clear()
            blogo()
        except:
            pass


#-----------------------------END BITNODES--------------------------------