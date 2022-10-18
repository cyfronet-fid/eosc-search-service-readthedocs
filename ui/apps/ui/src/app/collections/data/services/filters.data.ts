import { IFiltersConfig } from '../../repositories/types';
import { URL_PARAM_NAME } from './nav-config.data';

export const servicesFilters: IFiltersConfig = {
  id: URL_PARAM_NAME,
  filters: [
    {
      id: 'best_access_right',
      filter: 'best_access_right',
      label: 'Order type',
      type: 'multiselect',
    },
    {
      id: 'categories',
      filter: 'categories',
      label: 'Categories',
      type: 'multiselect',
    },
    {
      id: 'scientific_domains',
      filter: 'scientific_domains',
      label: 'Scientific Domains',
      type: 'multiselect',
    },
    {
      id: 'providers',
      filter: 'providers',
      label: 'Providers',
      type: 'multiselect',
    },
    {
      id: 'resource_organisation',
      filter: 'resource_organisation',
      label: 'Resource organisation',
      type: 'multiselect',
    },
    {
      id: 'dedicated_for',
      filter: 'dedicated_for',
      label: 'Dedicated for',
      type: 'multiselect',
    },
    {
      id: 'related_platforms',
      filter: 'related_platforms',
      label: 'Related infrastructures and platforms',
      type: 'multiselect',
    },
    {
      id: 'rating',
      filter: 'rating',
      label: 'Rating',
      type: 'multiselect',
    },
    {
      id: 'geographical_availabilities',
      filter: 'geographical_availabilities',
      label: 'Country',
      type: 'multiselect',
    },
    {
      id: 'language',
      filter: 'language',
      label: 'Language',
      type: 'tag',
    },
  ],
};