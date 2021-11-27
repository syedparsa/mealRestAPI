# Meal API

Meal API is a REST API made in Flask to get meals.

##**How to use this APi**
please use the cURL command to create admin/user, login
and acces the meals data as user/admin 

logIn as admin to make amendments in the MealsAPI data create/add/delete/update informations stored int the API

As a user one can only access/consume meals data in the API

######*Creating NEW USEr*

curl --location --request POST 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data-raw '{
 "name":"Mark","password":"Mark@9944"
}'

##################Login User####

curl --location --request POST 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic TWFyazpNYXJrQDk5NDQ=' \
--data-raw '{
 "name":"Mark","password":"Mark@9944"
}'

########User gets meals data form API##

curl --location --request GET 'http://127.0.0.1:5000/meal' \
--header 'Content-Type: application/json' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZXhwIjoxNjM3OTY4MjY1fQ.V9pWDTAIbabqcqW_CbiEYMOpBpB06beL_Kj735TGqbQ' \
--header 'Authorization: Basic TWFyazpNYXJrQDk5NDQ='


#####Creating a new Admin##



curl --location --request POST 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic Og==' \
--data-raw '{

    "name":"zeeshan","password":"muhammad@12"
}'


######Admin Login(using previous admin for login)###

curl --location --request GET 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRpbDphZGlsQA=='

####Creating new meals as a Admin###

curl --location --request POST 'http://127.0.0.1:5000/createMeal' \
--header 'Content-Type: application/json' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZXhwIjoxNjM3OTY5OTQ1fQ.Xu4CPfAUg7fDgaNHB85IJ1QQbGEcl0vGfm5pXswtxOQ' \
--data-raw '{
 
"name":"onion Pakoray",
"price":"1500",
"isSpicy":1,
"isVegan":1,
"ingredients":"potato,spices,grill onions",
"isGlutenFree":0,
"description":"Lahori chat masala taste extra spicy"


}
'
####Updating Meals as Admin###

curl --location --request POST 'http://127.0.0.1:5000/updateMeal/1' \
--header 'Content-Type: application/json' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZXhwIjoxNjM3OTY5OTQ1fQ.Xu4CPfAUg7fDgaNHB85IJ1QQbGEcl0vGfm5pXswtxOQ' \
--data-raw '{
 

"price":"2500",
"isSpicy":1,
"isVegan":1,
"ingredients":"potato,grill onions",
"isGlutenFree":1,
"description":"sweet onion pakora"


}
'



###updating Meal by its name##

curl --location --request POST 'http://127.0.0.1:5000/updateMeal/biryani' \
--header 'Content-Type: application/json' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZXhwIjoxNjM3OTY5OTQ1fQ.Xu4CPfAUg7fDgaNHB85IJ1QQbGEcl0vGfm5pXswtxOQ' \
--data-raw '{
 

"price":"500",
"isSpicy":1,
"isVegan":1,
"ingredients":"chicken,rice,pakistanispices onions",
"isGlutenFree":0,
"description":"sindhi biryaani,extra hot "


}
'

#### Deleting Meal as Admin##
curl --location --request DELETE 'http://127.0.0.1:5000/meal/1' \
--header 'Content-Type: application/json' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZXhwIjoxNjM3OTY5OTQ1fQ.Xu4CPfAUg7fDgaNHB85IJ1QQbGEcl0vGfm5pXswtxOQ' \
--data-raw '{
 

"price":"500",
"isSpicy":1,
"isVegan":1,
"ingredients":"chicken,rice,pakistanispices onions",
"isGlutenFree":0,
"description":"sindhi biryaani,extra hot "


}
'

####Accessing all Users details as admin###
curl --location --request GET 'http://127.0.0.1:5000/users' \
--header 'Content-Type: application/json' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZXhwIjoxNjM3OTY5OTQ1fQ.Xu4CPfAUg7fDgaNHB85IJ1QQbGEcl0vGfm5pXswtxOQ' \
--header 'Authorization: Basic YWRpbDphZGlsQA=='





## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)