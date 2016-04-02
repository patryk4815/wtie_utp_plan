Requirements
============

* Python 3.5+

Instalation
===========

.. code-block:: python

    git clone https://github.com/patryk4815/wtie_utp_plan.git
    cd wtie_utp_plan
    pip3.5 install -r requirements.txt


Configuring
===========

* https://github.com/patryk4815/wtie_utp_plan/blob/master/main.py#L59
* change ours email
* add script to ``crontab -e``
``
30 */6 * * * python3.5 /home/patryk/wtie_utp_plan/main.py 2&> /dev/null
``

Run
===

.. code-block:: python

    cd wtie_utp_plan
    python3.5 main.py
