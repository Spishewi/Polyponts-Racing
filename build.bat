pygbag --template ./src/pygbag.tmpl --title Polyponts-Racing --app_name Polyponts-Racing --build ./src
git add src/build/web/*
git commit -m "building for web"
git subtree push --prefix src/build/web origin gh-pages
