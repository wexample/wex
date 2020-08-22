
demoProgress() {
  wex render/progressBar -w=30 -p=10 -s="First step down"
  wex render/progressBar -w=30 -p=50 -s="Middle step done"
  wex render/progressBar -w=30 -p=100 -s="Complete"
}