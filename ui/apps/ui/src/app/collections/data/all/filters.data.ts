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
      id: 'unified_categories',
      filter: 'unified_categories',
      label: 'Research step',
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
      id: 'doi',
      filter: 'doi',
      label: 'DOI',
      type: 'tag',
    },
    {
      id: 'scientific_domains',
      filter: 'scientific_domains',
      label: 'Scientific Domains',
      type: 'tag',
    },
    {
      id: 'resource_organisation',
      filter: 'resource_organisation',
      label: 'Resource organisation',
      type: 'tag',
    },
    {
      id: 'keywords',
      filter: 'keywords',
      label: 'Keywords',
      type: 'tag',
    },
    {
      id: 'tag_list',
      filter: 'tag_list',
      label: 'Keywords',
      type: 'tag',
    },
  ],
};
