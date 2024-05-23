creating_migration () 
{
  pipenv run init
  pipenv run migrate
  pipenv run upgrade
}

migrate_upgrade () 
{
  pipenv run migrate
  pipenv run upgrade
}

dir=$(pwd)

if [ ! -d $dir/migrations ]
then
echo 'creating migration'
creating_migration
else
echo 'migrations already created'
echo 'updating migrations'
migrate_upgrade
fi