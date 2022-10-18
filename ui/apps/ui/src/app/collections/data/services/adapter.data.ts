import { IAdapter, IResult } from '../../repositories/types';
import { URL_PARAM_NAME } from './nav-config.data';
import { IService } from './service.model';
import { COLLECTION } from './search-metadata.data';

export const servicesAdapter: IAdapter = {
  id: URL_PARAM_NAME,
  adapter: (service: Partial<IService> & { id: string }): IResult => ({
    id: service.id,
    // basic information
    title: service.title?.join(' ') || '',
    description: service.description?.join(' ') || '',
    type: service.type || '',
    url: service.pid
      ? `https://marketplace.eosc-portal.eu/services/${service.pid}`
      : '',
    collection: COLLECTION,
    coloredTag: [
      {
        value: service?.best_access_right || '',
        filter: 'best_access_right',
        colorClassName: (service?.best_access_right || '').match(
          /open(.access)?/gi
        )
          ? 'tag-light-green'
          : 'tag-light-coral',
      },
      {
        colorClassName: 'tag-peach',
        filter: 'language',
        value: service?.language || [],
      },
    ],
    tags: [
      {
        label: 'Scientific domain',
        value: service.scientific_domains || [],
        filter: 'scientific_domains',
      },
      {
        label: 'Organisation',
        value: service.resource_organisation || '',
        filter: 'resource_organisation',
      },
    ],
  }),
};