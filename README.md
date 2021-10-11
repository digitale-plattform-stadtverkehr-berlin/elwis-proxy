# Elwis Proxy

Der Webservice ruft die Meldungen für die Binneschifffahrt von https://www.elwis.de ab,
und liefert die Meldungen die Berlin und Umgebung betreffen als GeoJSON zurück.

Abgefragt werden nur aktuell gültige Meldungen. Die Daten werden einmal pro Stunde aktualisiert.

:warning: Die verwendete Schnittstelle zum Abrufen der Daten ist nicht publiziert und kann sich jederzeit ändern.
Es wird empfohlen die Schnittstelle unter https://nts.elwis.de/server/MessageServer.php?WSDL zu verwenden.

Das Urheberrecht und die Nutzungsrechte der verarbeiteten Inhalte liegen bei der Wasserstraßen- und Schifffahrtsverwaltung des Bundes (WSV).
https://www.elwis.de/DE/Service/Haftungsausschluss-und-Nutzungsbedingungen/Haftungsausschluss-und-Nutzungsbedingungen-node.html

## Parameter

* **HOST** - Hostname des Servers - Default:```localhost```
* **PORT** - Port der Anwendung - Default:```8000```

## Docker Image bauen und in GitHub Registry pushen

```bash
> docker build -tdocker.pkg.github.com/digitale-plattform-stadtverkehr-berlin/elwis-proxy/elwis-proxy:<TAG> .
> docker push docker.pkg.github.com/digitale-plattform-stadtverkehr-berlin/elwis-proxy/elwis-proxy:<TAG>
```
