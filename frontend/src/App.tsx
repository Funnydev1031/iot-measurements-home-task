/** @format */

import React from 'react';
import useFetch from './hooks/useFetch';
import { ILocation } from './types/Location';
import { IDevice } from './types/Device';

type ILocationAndDevice = ILocation & { devices: Array<string> };

const BACKEND_BASE_URL = `http://localhost:65000`;
export const App: React.FunctionComponent = () => {
  const {
    data: locations,
    error: locationError,
    loading: locationLoading,
  } = useFetch(BACKEND_BASE_URL + '/locations');

  const {
    data: devices,
    error: deviceError,
    loading: deviceLoading,
  } = useFetch(BACKEND_BASE_URL + '/devices');

  let locationAndDevice: ILocationAndDevice;
  const locationsAndDevices = locations.map((location: ILocation) => {
    locationAndDevice = { ...location, devices: [] };
    devices.forEach((device: IDevice) => {
      if (device.location_id === location.id) {
        locationAndDevice.devices.push(device.mac);
      }
    });
    return locationAndDevice;
  });

  return (
    <>
      {(locationLoading || deviceLoading) && 'loading...'}
      <table>
        <thead>
          <tr>
            <th>Location</th>
            <th>Device</th>
          </tr>
        </thead>
        <tbody>
          {locationsAndDevices.length &&
            locationsAndDevices.map((element: ILocationAndDevice) => (
              <tr key={element.id}>
                <td>{element.name}</td>
                <td>
                  {element.devices.length &&
                    element.devices.map((device) => <div key={device}>{device}</div>)}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
      <p>{!locationsAndDevices.length && locationError && 'Location Loading Error...'}</p>
      <p>{!locationsAndDevices.length && deviceError && 'Device Loading Error...'}</p>
    </>
  );
};
