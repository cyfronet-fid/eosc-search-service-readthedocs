import { IAdapter, IResult } from '../../repositories/types';
import { URL_PARAM_NAME } from './nav-config.data';
import { COLLECTION } from './search-metadata.data';
import { IOpenAIREResult } from '@collections/data/openair.model';
import moment from 'moment';
import { IDataSource } from '@collections/data/data-sources/data-source.model';
import { ITraining } from '@collections/data/trainings/training.model';
import { IGuideline } from '@collections/data/guidelines/guideline.model';
import { IService } from '@collections/data/services/service.model';
import { hackDataSourceUrl } from '@collections/data/data-sources/adapter.data';
import {
  toArray,
  toValueWithLabel,
} from '@collections/filters-serializers/utils';
import {
  toAccessRightColoredTag,
  toBetaTag,
  toHorizontalServiceTag,
  toLanguageColoredTag,
} from '@collections/data/shared-tags';
import {
  parseStatistics,
  toKeywordsSecondaryTag,
} from '@collections/data/utils';
import { ConfigService } from '../../../services/config.service';

const urlAdapter = (
  type: string,
  data: Partial<
    IOpenAIREResult & IDataSource & IService & ITraining & IGuideline
  >
) => {
  switch (type) {
    case 'dataset':
    case 'publication':
    case 'software':
    case 'other':
      return `${
        ConfigService.config?.eosc_explore_url
      }/search/result?id=${data?.id?.split('|')?.pop()}`;
    case 'data source':
      return hackDataSourceUrl(data?.pid);
    case 'service':
      return `${ConfigService.config?.marketplace_url}/services/${data?.pid}`;
    case 'training':
      return '/trainings/' + data.id;
    case 'interoperability guideline':
      return '/guidelines/' + data.id;
    default:
      return '';
  }
};

export const allCollectionsAdapter: IAdapter = {
  id: URL_PARAM_NAME,
  adapter: (
    data: Partial<
      IOpenAIREResult & ITraining & IDataSource & IService & IGuideline
    > & {
      id: string;
    }
  ): IResult => ({
    id: data.id,
    title: data?.title?.join(' ') || '',
    description: data?.description?.join(' ') || '',
    date: data['publication_date']
      ? moment(data['publication_date']).format('DD MMMM YYYY')
      : '',
    url: urlAdapter(data.type || '', data),
    coloredTags: [
      toHorizontalServiceTag(data?.horizontal),
      toAccessRightColoredTag(data?.best_access_right),
      toLanguageColoredTag(data?.language),
    ],
    tags: [
      {
        label: 'Author names',
        values: toValueWithLabel(toArray(data?.author_names)),
        filter: 'author_names',
      },
      {
        label: 'DOI',
        values: toValueWithLabel(toArray(data?.doi)),
        filter: 'doi',
      },
      {
        label: 'Scientific domain',
        values: toValueWithLabel(toArray(data?.scientific_domains)),
        filter: 'scientific_domains',
      },
      {
        label: 'Organisation',
        values: toValueWithLabel(toArray(data?.resource_organisation)),
        filter: 'resource_organisation',
      },
    ],
    type: {
      label: data.type || '',
      value: (data.type || '')?.replace(/ +/gm, '-'),
    },
    collection: COLLECTION,
    secondaryTags: [
      // toDownloadsStatisticsSecondaryTag(data.usage_counts_downloads),
      // toViewsStatisticsSecondaryTag(data.usage_counts_views),
      toKeywordsSecondaryTag(data.keywords ?? [], 'keywords'),
      toKeywordsSecondaryTag(data.tag_list ?? [], 'tag_list'),
    ],
    ...parseStatistics(data),
  }),
};
