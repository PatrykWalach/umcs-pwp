from __future__ import annotations

import http.client
import json
import urllib.request

if __name__ == "__main__":
    response: http.client.HTTPResponse = urllib.request.urlopen(
        urllib.request.Request(
            "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=51.246452&lon=22.568445",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            },
        )
    )

    data = json.loads(response.read().decode("utf-8"))
    print(data)
    units = data["properties"]["meta"]["units"]

    for timeserie in data["properties"]["timeseries"][0::12]:
        details = timeserie["data"]["instant"]["details"]

        print(timeserie["time"])
        air_temperature = details["air_temperature"]
        print(f"\t{air_temperature}" + units["air_temperature"])
        air_pressure_at_sea_level = details["air_pressure_at_sea_level"]
        print(f"\t{air_pressure_at_sea_level}" + units["air_pressure_at_sea_level"])
