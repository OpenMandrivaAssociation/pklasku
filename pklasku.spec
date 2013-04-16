Summary:	PkLasku - Web application to create Finnish invoices
Name:		pklasku
Version:	1.0.4
Release:	4
License:	GPLv2
Group:		System/Servers
URL:		http://pklasku.sourceforge.net/
Source:		%name-%version.tar.gz
Requires:	apache-mod_php
Requires:	php-mysql
BuildArch:	noarch

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

install -d -m755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
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



%files
%defattr(-,root,root)
%doc INSTALL LICENSE gpl.txt README.install.urpmi
%config(noreplace) %{_webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/sqlfuncs.php
%{_datadir}/%{name}
%{_var}/www/%{name}




%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-2mdv2011.0
+ Revision: 614561
- the mass rebuild of 2010.1 packages

* Tue Mar 02 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.0.4-1mdv2010.1
+ Revision: 513670
- fix license
- update to 1.0.4

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.3-3mdv2010.1
+ Revision: 501750
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.0.3-2mdv2010.0
+ Revision: 430738
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 1.0.3-1mdv2009.0
+ Revision: 140731
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jul 19 2007 Anssi Hannula <anssi@mandriva.org> 1.0.3-1mdv2008.0
+ Revision: 53418
- 1.0.3


* Sun Jan 21 2007 Anssi Hannula <anssi@mandriva.org> 1.0.2-1mdv2007.0
+ Revision: 111485
- 1.0.2
- Import pklasku

* Mon Jun 12 2006 Anssi Hannula <anssi@mandriva.org> 1.0.1-1mdv2007.0
- 1.0.1

* Mon Jun 05 2006 Anssi Hannula <anssi@mandriva.org> 1.0-1mdv2007.0
- initial Mandriva release

