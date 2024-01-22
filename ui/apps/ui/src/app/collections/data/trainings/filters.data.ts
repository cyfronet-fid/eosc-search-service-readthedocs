import { IFiltersConfig } from '../../repositories/types';
import { URL_PARAM_NAME } from './nav-config.data';
import {
  alphanumericFilterSort,
  transformCatalogueNames,
} from '@collections/data/utils';

export const trainingsFilters: IFiltersConfig = {
  id: URL_PARAM_NAME,
  filters: [
    {
      id: 'unified_categories',
      filter: 'unified_categories',
      label: 'Research step',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'best_access_right',
      filter: 'best_access_right',
      label: 'Access right',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'scientific_domains',
      filter: 'scientific_domains',
      label: 'Scientific domain',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'resource_type',
      filter: 'resource_type',
      label: 'Resource type',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'content_type',
      filter: 'content_type',
      label: 'Material type (format)',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'target_group',
      filter: 'target_group',
      label: 'Target group',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'language',
      filter: 'language',
      label: 'Language',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
      customSort: alphanumericFilterSort,
    },
    {
      id: 'resource_organisation',
      filter: 'resource_organisation',
      label: 'Organisation',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'publication_date',
      filter: 'publication_date',
      label: 'Date range',
      type: 'date-calendar',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'duration',
      filter: 'duration',
      label: 'Duration',
      type: 'range',
      defaultCollapsed: false,
      tooltipText: '',
    },

    {
      id: 'level_of_expertise',
      filter: 'level_of_expertise',
      label: 'Level of expertise',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },

    {
      id: 'license',
      filter: 'license',
      label: 'License',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },

    {
      id: 'format',
      filter: 'format',
      label: 'Format',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'qualification',
      filter: 'qualification',
      label: 'Qualification',
      type: 'multiselect',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'author_names',
      filter: 'author_names',
      label: 'Authors',
      type: 'tag',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'keywords',
      filter: 'keywords',
      label: 'Keywords',
      type: 'tag',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'license',
      filter: 'license',
      label: 'License',
      type: 'tag',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'keywords',
      filter: 'keywords',
      label: 'Keywords',
      type: 'tag',
      defaultCollapsed: false,
      tooltipText: '',
    },
    {
      id: 'catalogue',
      filter: 'catalogue',
      label: 'Community Catalog',
      type: 'dropdown',
      defaultCollapsed: false,
      tooltipText: '',
      global: true,
      transformNodes: transformCatalogueNames,
    },
  ],
};
