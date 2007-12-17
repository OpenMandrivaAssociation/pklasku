
%define name	pklasku
%define version	1.0.3
%define rel	1

%if %{mdkversion} < 1020
%define webappconfdir %{_sysconfdir}/httpd/conf.d
%else
%define webappconfdir %{_sysconfdir}/httpd/conf/webapps.d
%endif

Summary:	PkLasku - Web application to create Finnish invoices
Name:		%name
Version:	%version
Release:	%mkrel %rel
License:	GPL
Group:		System/Servers
URL:		http://pklasku.sourceforge.net/
Source:		%name-%version.tar.gz
BuildRequires:	apache-base >= 2.0.54-5mdk
BuildRequires:	dos2unix
Requires:	apache mod_php php-mysql
BuildArch:	noarch

%description
PkLasku is a web application written in PHP for printing Finnish
invoices. Among its features are automatic invoice numbering and
reference calculation, pdf generation, customer database and an
unlimited number of user accounts. Data is stored in SQL database.

%prep
%setup -q -n %name

dos2unix font/*.php font/makefont/makefont.php
chmod a-x gpl.txt font/*.php font/makefont/*.{map,php}

cat > README.install.urpmi <<EOF
1. Create an SQL database 'pklasku'.
2. Push the contents of %{_datadir}/%{name}/CREATESQL to the
   database. The file encoding is ISO-8859-1 (Latin-1).
3. Edit %{_sysconfdir}/%{name}/sqlfuncs.php to contain the correct
   SQL credentials.
4. Log in with default credentials admin admin.
5. Go to System->Käyttäjät and change the Administrator credentials.
6. If you use the interface through https://, change the protocol in
   the file %{_sysconfdir}/%{name}/sqlfuncs.php.
EOF

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{webappconfdir}
cat > %{buildroot}%{webappconfdir}/%{name}.conf <<EOF

Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
php_admin_value include_path      ".:%{_sysconfdir}/%{name}"
</Directory>
EOF

install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m755 %{buildroot}%{_var}/www/%{name}
install -d -m755 %{buildroot}%{_datadir}/%{name}

install -m644 *.php *.html *.css *.ico %{buildroot}%{_var}/www/%{name}
cp -a fi_images font %{buildroot}%{_var}/www/%{name}

mv %{buildroot}%{_var}/www/%{name}/sqlfuncs.php %{buildroot}%{_sysconfdir}/%{name}

install -m644 CREATESQL %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc INSTALL LICENSE gpl.txt README.install.urpmi
%config(noreplace) %{webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/sqlfuncs.php
%{_datadir}/%{name}
%{_var}/www/%{name}


