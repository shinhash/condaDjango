{% if query_id == 'selectSignUser' %}
    SELECT   USER_ID
           , USER_PW
           , USER_NM
           , REG_DT
           , REG_USER_ID
           , REG_IP
           , MOD_DT
           , MOD_USER_ID
           , MOD_IP
           , USE_YN
           , SNS_SIGN_ID
      FROM DJANGO_MARIADB.USERS
     WHERE USE_YN = 'Y'
       AND USER_ID = '{{ sign_id }}'
 {% endif %}