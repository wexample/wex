CI_JOB_TOKEN=glpat-PAHuLocqyf1ZGuY58GYb
CI_API_V4_URL="gitlab.wexample.com/api/v4"
CI_PROJECT_ID=155

# TODO rename ~ to -
curl --request PUT \
  --header "PRIVATE-TOKEN: ${CI_JOB_TOKEN}" \
  --upload-file "wex_5.0.0~beta.2-1_all.deb" \
  "https://${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/debian/wex/5.0.0-beta.2/wex_5.0.0-beta.2-1_all.deb"

#curl --request POST \
#  --header "PROJECT-TOKEN: ${CI_JOB_TOKEN}" \
#  --data-binary "@wex_5.0.0~beta.2-1_all.deb" \
#  "https://gitlab.wexample.com/wexample/wex/packages/debian/wex/pool/wex_5.0.0~beta.2-1_all.deb"

#curl --request POST \
#  --header "JOB-TOKEN: ${CI_JOB_TOKEN}" \
#  --data-binary "@${DEBIAN_PACKAGE_NAME}_${DEBIAN_PACKAGE_VERSION}_*.deb" \
#  "https://${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/debian/${DEBIAN_PACKAGE_NAME}/pool/${DEBIAN_PACKAGE_NAME}_${DEBIAN_PACKAGE_VERSION}_all.deb"