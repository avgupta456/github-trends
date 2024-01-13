if [ $# -eq 0 ]; then
    echo "Usage: $0 <mongodb_password>"
    exit 1
fi

# Export
mongoexport --uri "mongodb+srv://backend.aqlpb.mongodb.net/" --db dev_backend --collection secrets --username root --password "$1" > ./dev_secrets.json
mongoexport --uri "mongodb+srv://backend.aqlpb.mongodb.net/" --db dev_backend --collection users --username root --password "$1" > ./dev_users.json
mongoexport --uri "mongodb+srv://backend.aqlpb.mongodb.net/" --db dev_backend --collection user_months --username root --password "$1" > ./dev_user_months.json

mongoexport --uri "mongodb+srv://backend.aqlpb.mongodb.net/" --db prod_backend --collection secrets --username root --password "$1" > ./prod_secrets.json
mongoexport --uri "mongodb+srv://backend.aqlpb.mongodb.net/" --db prod_backend --collection users --username root --password "$1" > ./prod_users.json
mongoexport --uri "mongodb+srv://backend.aqlpb.mongodb.net/" --db prod_backend --collection user_months --username root --password "$1" > ./prod_user_months.json

# Import
mongoimport --uri "mongodb+srv://backend2.e50j8dp.mongodb.net/" --db dev_backend --collection secrets --username root --password "$1" < ./dev_secrets.json
mongoimport --uri "mongodb+srv://backend2.e50j8dp.mongodb.net/" --db dev_backend --collection users --username root --password "$1" < ./dev_users.json
mongoimport --uri "mongodb+srv://backend2.e50j8dp.mongodb.net/" --db dev_backend --collection user_months --username root --password "$1" < ./dev_user_months.json

mongoimport --uri "mongodb+srv://backend2.e50j8dp.mongodb.net/" --db prod_backend --collection secrets --username root --password "$1" < ./prod_secrets.json
mongoimport --uri "mongodb+srv://backend2.e50j8dp.mongodb.net/" --db prod_backend --collection users --username root --password "$1" < ./prod_users.json
mongoimport --uri "mongodb+srv://backend2.e50j8dp.mongodb.net/" --db prod_backend --collection user_months --username root --password "$1" < ./prod_user_months.json

# Remove
rm ./dev_secrets.json
rm ./dev_users.json
rm ./dev_user_months.json

rm ./prod_secrets.json
rm ./prod_users.json
rm ./prod_user_months.json