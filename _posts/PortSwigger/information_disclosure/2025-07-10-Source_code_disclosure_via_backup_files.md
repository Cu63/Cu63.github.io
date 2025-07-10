---
title: "Source code disclosure via backup files"
date: 2025-07-10
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-via-backup-files"
classes: wide
---

В данной лабораторной работе можно получить доступ к бекапу приложения. Для решения нужно найти пароль от БД.

```
https://0a0a001a0466aaaa80aa532600a8008c.web-security-academy.net/
```

## Solution

На самой странице не вижу ничего особо интересного. Попробую пофаззить страницы через `ffuf`:

```bash
cu63:~/ $ ffuf -u https://0a0a001a0466aaaa80aa532600a8008c.web-security-academy.net/FUZZ -w ~/wordlists/common.txt                                      

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://0a0a001a0466aaaa80aa532600a8008c.web-security-academy.net/FUZZ
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

analytics               [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 63ms]
backup                  [Status: 200, Size: 435, Words: 126, Lines: 17, Duration: 84ms]
favicon.ico             [Status: 200, Size: 15406, Words: 11, Lines: 1, Duration: 61ms]
filter                  [Status: 200, Size: 10877, Words: 5099, Lines: 200, Duration: 69ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Нашел интересную страницу — `backup`. Посмотрю, что же там)

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Source_code_disclosure_via_backup_files/1.png){: height="200" .align-center}

Скачаю файл:

```java
package data.productcatalog;

import common.db.JdbcConnectionBuilder;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ProductTemplate implements Serializable
{
    static final long serialVersionUID = 1L;

    private final String id;
    private transient Product product;

    public ProductTemplate(String id)
    {
        this.id = id;
    }

    private void readObject(ObjectInputStream inputStream) throws IOException, ClassNotFoundException
    {
        inputStream.defaultReadObject();

        ConnectionBuilder connectionBuilder = ConnectionBuilder.from(
                "org.postgresql.Driver",
                "postgresql",
                "localhost",
                5432,
                "postgres",
                "postgres",
                "any51oqtktpkqkoamc5rfyp44pa5lbig"
        ).withAutoCommit();
        try
        {
            Connection connect = connectionBuilder.connect(30);
            String sql = String.format("SELECT * FROM products WHERE id = '%s' LIMIT 1", id);
            Statement statement = connect.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);
            if (!resultSet.next())
            {
                return;
            }
            product = Product.from(resultSet);
        }
        catch (SQLException e)
        {
            throw new IOException(e);
        }
    }

    public String getId()
    {
        return id;
    }

    public Product getProduct()
    {
        return product;
    }
}
```

Это код на `Java` ~~терпеть ее не могу~~, который работает с БД. А креды находятся прямо в коде — `any51oqtktpkqkoamc5rfyp44pa5lbig`.

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Source_code_disclosure_via_backup_files/2.png){: height="200" .align-center}
