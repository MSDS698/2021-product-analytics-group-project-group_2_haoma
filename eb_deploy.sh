<<<<<<< Updated upstream
eb init group-2-haoma-app -p Docker -r us-west-2
eb create group-2-haoma-env --envvar AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --envvar AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
=======
eb init group-2-haoma-app -p Docker -r us-west-2 --keyname=$PEM_NAME
eb create group-2-haoma-env --instance_type t2.large --envvar AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --envvar AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
>>>>>>> Stashed changes
