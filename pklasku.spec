%define name	pklasku
%define version	1.0.4
%define rel	1

Summary:	PkLasku - Web application to create Finnish invoices
Name:		%name
Version:	%version
Release:	%mkrel %rel
License:	GPLv2
Group:		System/Servers
URL:		http://pklasku.sourceforge.net/
Source:		%name-%version.tar.gz
Requires:	apache-mod_php
Requires:	php-mysql
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
PkLasku is a web application written in PHP for printing Finnish
invoices. Among its features are automatic invoice numbering and
reference calculation, pdf generation, customer database and an
unlimited number of user accounts. Data is stored in SQL database.

%prep
%setup -q -n %name

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
    Order allow,deny
    Allow from all
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
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc INSTALL LICENSE gpl.txt README.install.urpmi
%config(noreplace) %{webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/sqlfuncs.php
%{_datadir}/%{name}
%{_var}/www/%{name}


