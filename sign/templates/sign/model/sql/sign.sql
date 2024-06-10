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
     WHERE USER_ID = '{{ sign_id }}'
{% endif %}


{% if query_id == 'insertSignUser' %}
    INSERT INTO DJANGO_MARIADB.USERS(
                  USER_ID
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
            )
            VALUES(
                  '{{ sign_id }}'
                , '{{ sign_pw }}'
                , '{{ name }}'
                , DATE_FORMAT(SYSDATE(), '%Y%m%d%H%i%s')
                , '{{ sign_id }}'
                , '127.0.0.1'
                , DATE_FORMAT(SYSDATE(), '%Y%m%d%H%i%s')
                , '{{ sign_id }}'
                , '127.0.0.1'
                , 'Y'
                , ''
            )
{% endif %}