aws configure import --csv file://credentials.csv
aws configure set region us-west-2
export AWS_PROFILE=$(cat credentials.csv | cut -f 1 -d ',' | tail -1)

curl https://data.cms.gov/provider-data/sites/default/files/resources/35759790ad0a207f47ba2a079eb51a0f_1620794404/HH_Zip_Oct2020.csv > HH_Zip_Oct2020.csv
echo "HH_Zip_Oct2020.csv has been downloaded..."
aws s3api put-object --bucket haoma-bucket --key HH_Zip_Oct2020.csv --body HH_Zip_Oct2020.csv
echo "HH_Zip_Oct2020.csv has been uploaded to S3 bucket 'haoma-bucket'..."
rm HH_Zip_Oct2020.csv
echo "HH_Zip_Oct2020.csv deleted from local dir..."

curl https://data.cms.gov/provider-data/sites/default/files/resources/1ee6a6e80907bf13661aa2f099415fcd_1620794404/HH_Provider_Oct2020.csv > HH_Provider_Oct2020.csv
echo "HH_Provider_Oct2020.csv has been downloaded..."
aws s3api put-object --bucket haoma-bucket --key HH_Provider_Oct2020.csv --body HH_Provider_Oct2020.csv
echo "HH_Provider_Oct2020.csv has been uploaded to S3 bucket 'haoma-bucket'..."
rm HH_Provider_Oct2020.csv
echo "HH_Provider_Oct2020.csv deleted from local dir..."

echo "Done"