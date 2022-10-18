import { IFiltersConfig } from '../../repositories/types';
import { URL_PARAM_NAME } from './nav-config.data';

export const allCollectionsFilters: IFiltersConfig = {
  id: URL_PARAM_NAME,
  filters: [
    {
      id: 'type',
      filter: 'type',
      label: 'Type of product',
      type: 'multiselect',
    },
    {
      id: 'best_access_right',
      filter: 'best_access_right',
      label: 'Access right',
      type: 'multiselect',
    },
    {
      id: 'fos',
      filter: 'fos',
      label: 'Scientific discipline',
      type: 'multiselect',
    },
    {
      id: 'language',
      filter: 'language',
      label: 'Language',
      type: 'multiselect',
    },
    {
      id: 'author_names',
      filter: 'author_names',
      label: 'Author names',
      type: 'tag',
    },
    {
      id: 'url',
      filter: 'url',
      label: 'DOI',
      type: 'tag',
    },
  ],
};