<html>
<head>
  <title>Wexample server</title>
  <style>
    body {
      padding: 20px;
    }

    #page {
      padding: 20px;
    }

    h1 {
      margin: 0;
    }

    p.hosts {
      padding: 10px;
      border: 1px dotted #CCC;
      border-radius: 10px;
    }

    .logo img {
      width: 160px;
      image-rendering: optimizeSpeed; /* STOP SMOOTHING, GIVE ME SPEED  */
      image-rendering: -moz-crisp-edges; /* Firefox                        */
      image-rendering: -o-crisp-edges; /* Opera                          */
      image-rendering: -webkit-optimize-contrast; /* Chrome (and eventually Safari) */
      image-rendering: pixelated; /* Chrome */
      image-rendering: optimize-contrast; /* CSS3 Proposed                  */
      -ms-interpolation-mode: nearest-neighbor; /* IE8+                           */
    }
  </style>
</head>
<body>
<h1>Wexample server</h1>
<section id="page">
  <div class="logo">
    <img src="logo.gif">
  </div>
    <?php

    $domains = trim(file_get_contents('/tmp/wexample/proxy/hosts'));

    ?>
  <p>Welcome to your server.

      <?php if ($domains) :?>
      You can edit your local host file by adding
    the lines bellow.</p>
  <p class="hosts"><?php print nl2br($domains); ?></p>
    <ul>
        <li>On <b>Windows</b> : C:\Windows\System32\drivers\etc\hosts</li>
        <li>On <b>Linux</b> : /etc/hosts
            <ul>
                <li><code>echo -e "\n# network.wex \n<?php echo str_replace("\t",' ', str_replace("\n",'\n', $domains)) ?>" >> /etc/hosts</code></li>
            </ul>
        </li>
    </ul>
    <?php

    $exp = explode("\n", $domains);

    ?>
  <p>Once change made, you could access to your sites by
    clicking these links.</p>
  <ul>
      <?php
      foreach ($exp as $line) {
          $line = trim($line);
          if ($line) {
              $line = explode("\t", $line);
              ?>
            <li>
              <a target="_blank"
                 href="http://<?php echo $line[1]; ?>"><?php echo $line[1]; ?></a>
            </li>
              <?php
          }
      }

      ?></ul>
    <?php else: ?>
      No site is running.
    <?php endif; ?>
</section>
</body>
</html>
