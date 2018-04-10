from flask import Flask
import couchdb,base64

couchserver = couchdb.Server("http://127.0.0.1:5984/")
dbname ="einfach_ambulant"
db=couchserver[dbname]

for doc in db:
    if db[doc]["subject_Type"]=="user":
        if "FrauPfleger" in db[doc]["username"]:
            id =db[doc].id
            #print(db[doc]["username"],db[id]["password"])

    #if db[doc]["subject_Type"] == "patient":
        #print(db[doc]['patient_name'])
k= db.get_attachment("b3482ca99c50284793c745341f018e10","wundprotokoll.png")
#print(k)
url="http://127.0.0.1:5984//einfach_ambulant/b3482ca99c50284793c745341f018e10/wundprotokoll"
for doc in db:
    if db[doc]["subject_Type"]=="document":
            if db[doc]["doc_type"] =="wundanamnese":
                id =db[doc].id

                print(db.get(id)["user_name"])



