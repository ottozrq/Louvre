import { config } from './api';

export const lang: string = "cn";

export const getTranslate = (obj?: object) => {
    if (obj) {
        const parsed = JSON.parse(JSON.stringify(obj))
        return parsed ? parsed[lang] ? parsed[lang] : parsed["en"] : "";
    }
    return ""

}

export const getImageUrl = (uri?: string) => {
    if (uri)
        return (config.basePath ? config.basePath : "") + "/images/" + uri;
    return ""
}