
demoChoice() {
  local ARR="one,two,three,a,b,c,d,e,f,g,h,i,j,k,l or m,n,o,p,q,r,s,t,u,v,etc"
  local VALUE;

  # Ask
  wex prompt/choice -c="${ARR}"

  # Retrieve
  VALUE=$(wex prompt/choiceGetValue)

  # Display
  _wexItemSuccess "You choosed: " "${VALUE}"

  echo ""
}
