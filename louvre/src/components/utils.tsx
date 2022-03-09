import { SetStateAction, useCallback, useEffect, useRef, useState } from 'react';

import { config } from './api';

export const lang: string = "cn";

export const getTranslate = (obj?: object) => {
    if (obj) {
        const parsed = JSON.parse(JSON.stringify(obj))
        return parsed ? parsed[lang] ? parsed[lang] : parsed["en"] : "";
    }
    return ""
}

export const toJson = (obj?: object) => {
    if (obj)
        return JSON.parse(JSON.stringify(obj))
    return {}
}

export const getImageUrl = (uri?: string) => {
    if (uri)
        return (config.basePath ? config.basePath : "") + "/images/" + uri;
    return ""
}

type Callback<T> = (value?: T) => void;
type DispatchWithCallback<T> = (value: T, callback?: Callback<T>) => void;

function useStateCallback<T>(initialState: T | (() => T)): [T, DispatchWithCallback<SetStateAction<T>>] {
  const [state, _setState] = useState(initialState);

  const callbackRef = useRef<Callback<T>>();
  const isFirstCallbackCall = useRef<boolean>(true);

  const setState = useCallback((setStateAction: SetStateAction<T>, callback?: Callback<T>): void => {
    callbackRef.current = callback;
    _setState(setStateAction);
  }, []);

  useEffect(() => {
    if (isFirstCallbackCall.current) {
      isFirstCallbackCall.current = false;
      return;
    }
    callbackRef.current?.(state);
  }, [state]);

  return [state, setState];
}

export default useStateCallback;